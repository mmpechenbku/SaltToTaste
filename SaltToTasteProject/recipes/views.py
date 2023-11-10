from datetime import datetime

from django.db.models import Prefetch, Count
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from .models import Recipe, Ingredient, SaveRecipe, CommentRecipe

from django.http import JsonResponse

from  .forms import CommentCreateForm, RecipeForm, StepForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


def add_recipe(request):
    if request.method == 'POST':
        title = request.POST['title']
        ingredients = request.POST['ingredients']
        instructions = request.POST['instructions']
        cooking_time = request.POST['cooking_time']

        recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, cooking_time=cooking_time)
        recipe.save()

        return redirect('recipe_list')

class AddingRecipe(CreateView):
    model = Recipe
    # form_class = AddingRecipeForm
    template_name = ''
    success_url = ''


def add_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        step_texts = request.POST.getlist('steps-text[]')
        step_images = request.FILES.getlist('steps-image[]')

        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            for text, image in zip(step_texts, step_images):
                step = StepForm({'description': text})
                if step.is_valid():
                    step_instance = step.save(commit=False)
                    step_instance.recipe = recipe
                    step_instance.image = image
                    step_instance.save()

    else:
        recipe_form = RecipeForm()

    return render(request, '', {'recipe_form': recipe_form,})


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = ''
    context_object_name = 'recipe'
    queryset = model.objects.detail()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['form'] = CommentCreateForm
        return context


def search_recipes(request):
    message = 'Всего рецептов: '
    selected_ingredient_ids = request.POST.get('ingredients', '').split(',')
    difficulty = request.POST.get('difficulty', '')
    time = request.POST.get('time', '')
    fullHit = request.POST.get('coincidence')

    #  selected_ingredient_ids не пуст и не содержит пустых значений
    selected_ingredient_ids = [id for id in selected_ingredient_ids if id]

    recipes = Recipe.objects.all()
    percentsDict = []

    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)

    if time:
        time = int(time)
        hours = time // 60
        minutes = time % 60
        time =  "{:02}:{:02}".format(int(hours), int(minutes))
        time = datetime.strptime(time, "%H:%M").time()

        recipes = recipes.filter(cookingTime__lte=time)

    if selected_ingredient_ids:
        recipes = Recipe.objects.filter(ingredients__id__in=selected_ingredient_ids).distinct()

        if difficulty:
            recipes = recipes.filter(difficulty=difficulty)

        if time:
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
                percentsDict.append({ recipe : percents })
        recipes = filtered_recipes
        message = 'Найдено рецептов: '

    # print(percentsDict)
    ingredients = Ingredient.objects.all()
    num_recipes = f"{message}{len(recipes)}"

    data = {
        'recipes' : recipes,
        'ingredients' : ingredients,
        'num_recipes' : num_recipes,
        'percentsDict' : percentsDict,
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
        # ip_address = get_client_ip(request)
        user = request.user if request.user.is_autentificated else None

        save, created = self.model.objects.get_of_create(
            recipe_id = recipe_id,
            user = user
        )

        if not created:
            save.delete()
            return JsonResponse({'status': 'deleted', 'save_sum': save.recipe.get_sum_save()})

        return JsonResponse({'status': 'created', 'save_sum': save.recipe.get_sum_save()})


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
                'author': comment.parent_id,
                'time_create': comment.time_create.strftime('%Y-%b-%d %H:%M:%S'),
                'avatar': comment.author.avatar.url,
                'content': comment.content,
                'get_absolute_url': comment.author.get_absolute_url()
            }, status=200)

        return redirect(comment.recipe.get_absolute_url())

    def handle_no_permission(self):
        return JsonResponse({'error': 'need authorisation'}, status=400)