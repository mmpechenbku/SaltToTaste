from datetime import datetime

from django.db.models import Prefetch, Count
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from .models import Recipe, Ingredient, SaveRecipe, CommentRecipe, RecipeStep, IngredientQuantity, Selection, LikeComment
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from .forms import CommentCreateForm, RecipeForm, StepForm, IngredientQuantityForm, IngredientQuantityFormSet, \
    StepFormSet
from django.contrib.auth.mixins import LoginRequiredMixin

import bs4


# Create your views here.

def index(request):
    recipes = Recipe.objects.all()
    saves = None
    if request.user.is_authenticated:
        saves = SaveRecipe.objects.filter(user=request.user).values_list('recipe', flat=True)

    data = {
        'recipes': recipes,
        'saves': saves,
    }
    return render(request, 'index.html', data)


# def recipe_detail(request):
#     return render(request, 'recipes/recipe_detail.html')


@login_required
def collections(request):
    return render(request, 'collections/collections.html')


def collections_detail(request):
    return render(request, 'collections/collections_detail.html')


class CollectionDetailView(DetailView):
    model = Selection
    template_name = 'collections/collections_detail.html'
    context_object_name = 'collection'
    #
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        recipes = [recipe for recipe in self.object.recipes.all()]

        recipe_ingr_dict = []
        for recipe in recipes:
            ingredients = []
            for ingredient in recipe.ingredients.all():
                ingredients.append(ingredient.name)
            recipe_ingr_dict.append({recipe: ingredients})

        context['recipes'] = recipes
        ingredients = [ingredient.name for ingredient in [recipe.ingredients for recipe in self.object.recipes.all()]]
        context['ingredients'] = ingredients
        context['recipes_ingr'] = recipe_ingr_dict
        context['saves'] = SaveRecipe.objects.filter(user=self.request.user).values_list('recipe', flat=True) if self.request.user.is_authenticated else None

        return context



@login_required
def selections(request):
    user = request.user
    selections = Selection.objects.filter(user=user)
    favorites = SaveRecipe.objects.filter(user=user)
    favorite_recipes = [favorite.recipe for favorite in favorites]
    data = {
        'selections': selections,
        'favorites': favorite_recipes,
    }
    return render(request, 'collections/collections.html', data)


def create_selection(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('title')
        print(name)
        picture = request.FILES.get('picture')
        print(picture)
        access = request.POST.get('access')
        print(access)
        # image = request.FILES.get('image')
        access = 'public' if access == 'on' else 'private'

        # Создаем новую подборку
        selection = Selection.objects.create(
            user=user,
            title=name,
            picture=picture,
            access=access,

            # image=image,
        )

        # Добавляем рецепты к подборке (если они выбраны в форме)
        recipe_ids = request.POST.getlist('recipes')
        recipes = Recipe.objects.filter(pk__in=recipe_ids)
        selection.recipes.set(recipes)

        # Возвращаем JSON-ответ с информацией о созданной подборке
        return JsonResponse({'status': 'success', 'collection_id': selection.id})
    else:
        # Возвращаем JSON-ответ с ошибкой, если метод запроса не POST
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    queryset = model.objects.detail()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title

        ingredients = []
        for ingredient in self.object.ingredients.all():
            ingredients.append(ingredient.name)

        context['ingredients'] = ingredients
        context['form'] = CommentCreateForm
        context['quantity_ingr'] = IngredientQuantity.objects.filter(recipe=self.object)
        context['saves'] = SaveRecipe.objects.filter(user=self.request.user).values_list('recipe', flat=True) if self.request.user.is_authenticated else None
        context['like_comments'] = LikeComment.objects.filter(user=self.request.user).values_list('comment', flat=True) if self.request.user.is_authenticated else None
        context['steps'] = RecipeStep.objects.filter(recipe=self.object).order_by('step_number')
        return context


def search_recipes(request):
    selected_ingredient_ids = request.POST.get('ingredients', '').split(',')
    difficulty = request.POST.get('difficulty', '')
    time = request.POST.get('time', '')
    fullHit = request.POST.get('coincidence')
    recipe_title = request.POST.get('title_search')
    sorting = request.POST.get('sorting')
    print(sorting)

    selected_ingredient_ids = [id for id in selected_ingredient_ids if id]

    recipes = Recipe.objects.popular()

    recipe_ingr_dict = []

    print(recipe_title)
    if recipe_title:
        recipes = recipes.filter(title__icontains=recipe_title)

    percentsDict = []

    if difficulty and difficulty != 'Все':
        print(difficulty)
        recipes = recipes.filter(difficulty=difficulty)

    if time and time != 0:
        time = int(time)
        hours = time // 60
        minutes = time % 60
        time = "{:02}:{:02}".format(int(hours), int(minutes))
        time = datetime.strptime(time, "%H:%M").time()

        recipes = recipes.filter(cookingTime__lte=time)

    if sorting and sorting != 0:
        if sorting != 'popularity':
            sorting = f'-{sorting}'
            recipes = recipes.order_by(sorting)

    for recipe in recipes:
        ingredients = []
        for ingredient in recipe.ingredients.all():
            ingredients.append(ingredient.name)
        recipe_ingr_dict.append({recipe: ingredients})

    if selected_ingredient_ids:
        recipes = Recipe.objects.filter(ingredients__id__in=selected_ingredient_ids).distinct()

        if difficulty and difficulty != 'Все':
            recipes = recipes.filter(difficulty=difficulty)

        if time and time != 0:
            recipes = recipes.filter(cooking_time__lte=time)



        # Фильтрация рецептов по процентному попаданию
        filtered_recipes = []
        percentsDict = []
        for recipe in recipes:
            total_ingredients = selected_ingredient_ids.__len__()
            ingredients_in_recipe = recipe.ingredients.count()
            matching_ingredients = recipe.ingredients.filter(id__in=selected_ingredient_ids).count()
            percentage = (matching_ingredients / ingredients_in_recipe) * 100
            comparisonPercents = 100 if fullHit else 70
            if percentage >= comparisonPercents:
                filtered_recipes.append(recipe)
                percents = f"{int(percentage)}%"
                percentsDict.append({recipe: percents})
        recipes = filtered_recipes

    ingredients = Ingredient.objects.all()
    num_recipes = str(len(recipes))

    saves = None

    if request.user.is_authenticated:
        saves = SaveRecipe.objects.filter(user=request.user)
        saves = saves.values_list('recipe', flat=True)

    data = {
        'recipes': recipes,
        'ingredients': ingredients,
        'num_recipes': num_recipes,
        'percentsDict': percentsDict,
        'recipes_ingr': recipe_ingr_dict,
        'saves': saves,
    }

    return render(request, 'recipes/recipe_search.html', data)


class IngredientSearchView(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        ingredients = Ingredient.objects.filter(name__icontains=search_query)
        data = [{'id': ingredient.id, 'name': ingredient.name} for ingredient in ingredients]
        return JsonResponse(data, safe=False)


class SaveRecipeCreateView(View):
    model = SaveRecipe

    def post(self, request, *args, **kwargs):
        recipe_id = request.POST.get('recipe_id')
        user = request.user if request.user.is_authenticated else None
        if user:
            save, created = self.model.objects.get_or_create(
                recipe_id=recipe_id,
                user=user
            )
            count = str(save.recipe.get_sum_save)
            print('count', count)
            print('save', save)
            print('recipe', save.recipe)
            if not created:
                save.delete()
                # print(save.recipe.get_sum_save())
                return JsonResponse({'status': 'deleted', 'save_sum': save.recipe.get_sum_save})

            return JsonResponse({'status': 'created', 'save_sum': save.recipe.get_sum_save})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = CommentRecipe
    form_class = CommentCreateForm

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({'error': form.errors}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.recipe_id = self.kwargs.get('pk')
        comment.author = self.request.user
        comment.parent_id = form.cleaned_data.get('parent')
        comment.save()

        if self.is_ajax():
            return JsonResponse({
                'is_child': comment.is_child_node(),
                'id': comment.id,
                'author': comment.author.username,
                'parent_id': comment.parent_id,
                'time_create': comment.time_create.strftime('%d %B %Y %H:%M'),
                'avatar': comment.author.avatar.url,
                'content': comment.content,
                'level': comment.level,
                'get_absolute_url': comment.author.get_absolute_url()
            }, status=200)
        return redirect(comment.recipe.get_absolute_url())

    def handle_no_permission(self):
        return JsonResponse({'error': 'need authorisation'}, status=400)


class LikeCommentCreateView(View):
    model = LikeComment

    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get('comment_id')
        user = request.user if request.user.is_authenticated else None
        if user:
            like, created = self.model.objects.get_or_create(
                comment_id=comment_id,
                user=user
            )
            if not created:
                like.delete()
                return JsonResponse({'status': 'deleted', 'likes_sum': like.comment.get_sum_likes()})
            return JsonResponse({'status': 'created', 'likes_sum': like.comment.get_sum_likes()})


def add_recipe(request):
    if request.method == 'POST':
        try:
            # Получаем данные из запроса
            recipe_name = request.POST.get('recipe_name')
            recipe_description = request.POST.get('recipe_description')
            recipe_image = request.FILES.get('recipe_image')
            difficulty = request.POST.get('difficulty')  # Получаем сложность
            cooking_time = request.POST.get('cooking_time')  # Получ
            ingredient_ids = request.POST.get('ingredients', '').split(',')
            ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
            # ... дополнительные поля ...

            print(recipe_name)
            print(recipe_description)
            print(recipe_image)
            print(difficulty)
            print(cooking_time)
            print(ingredients)

            # Создаем объект Recipe
            recipe = Recipe.objects.create(
                title=recipe_name,
                description=recipe_description,
                picture=recipe_image,
                difficulty=difficulty,
                cookingTime=cooking_time,
                author=request.user,
                # ingredients = ingredients,
                # ... дополнительные поля ...
            )
            recipe.ingredients.set(ingredients)

            # iter = 1
            for ingredient in ingredients:
                quantity = request.POST.get(f'quantity_{ingredient.id}')
                # iter += 1
                print(ingredient)
                print(quantity)

                IngredientQuantity.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=quantity
                )

            # Обработка шагов приготовления
            steps_count = int(request.POST.get('steps_count', 0))
            for i in range(1, steps_count + 1):
                step_description = request.POST.get(f'step_description_{i}')
                step_image = request.FILES.get(f'step_image_{i}')

                RecipeStep.objects.create(
                    recipe=recipe,
                    description=step_description,
                    image=step_image,
                    step_number=i
                )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    else:
        ingredients = Ingredient.objects.all()
        data = {
            'ingredients': ingredients
        }
        return render(request, 'recipes/recipe_add.html', data)

        # return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
