from django.db.models import Prefetch, Count
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from .models import Recipe, Ingredient
from .filters import RecipeFilter


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
    form_class = AddingRecipeForm
    template_name = ''
    success_url = ''

# class RecipesPage(ListView):
#     model = Recipe
#     context_object_name = 'recipe'
#     template_name = ''
#     paginate_by = 5
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['search_filter'] =

def search_recipes(request):
    ingredient_ids = request.GET.getlist('ingredients')
    ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
    prefetch = Prefetch('ingredients', queryset=ingredients, to_attr='selected_ingredients')
    recipes = Recipe.objects.filter(ingredients__in=ingredients).annotate(num_ingredients=Count('ingredients')).prefetch_related(prefetch)
    filtered_recipes = []
    for recipe in recipes:
        hit_percentage = len(set(recipe.selected_ingredients).intersection(ingredients)) / len(ingredients)
        if hit_percentage >= 0.7:
            filtered_recipes.append((recipe, hit_percentage))
    sorted_recipes = sorted(filtered_recipes, key=lambda x: x[1], reverse=True)
    return render(request, 'search_results.html', {'sorted_recipes': sorted_recipes})

# def search_recipes(request):
#     matched_recipes = Recipe.objects.all()
#
#     if request.method == 'GET':
#         ingredients = request.GET.get('ingredients').split(',')
#
#         recipes = Recipe.objects.filter(ingredients__name__in=ingredients)
#         total_ingredients = len(ingredients)
#
#         matched_recipes = []
#         for recipe in recipes:
#             matched_ingredients = recipe.ingredients.filter(name__in=ingredients).count()
#             if (matched_ingredients / total_ingredients) * 100 >= 70:
#                 matched_recipes.append(recipe)
#
#     return(matched_recipes)
#
#     # return render(request, 'search_results.html', {'matched_recipes': matched_recipes})
#
#     # return render(request, 'search_recipes.html')
#
# class RecipesPage(ListView):
#     model = Recipe
#     context_object_name = 'recipe'
#     template_name = ''
#     paginate_by = 5
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['search_filter'] = RecipeFilter(self.request.GET, queryset=search_recipes(self.request))
#         context['seatch_filter'] = RecipeFilter(self.request.GET, queryset=Recipe.objects.)
#         return context
#
#     def get_queryset(self):
#         queryset = search_recipes(self.request)
#         return RecipeFilter(self.request.GET, queryset=queryset).qs