from datetime import datetime

from django.db.models import Prefetch, Count
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView
from .models import Recipe, Ingredient

from django.http import JsonResponse
from django.db.models import Q
from .filters import RecipeFilter


# Create your views here.

def recipe_detail(request):
    return render(request, 'recipes/recipe_detail.html')


def collections(request):
    return render(request, 'collections/collections.html')


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

def search_recipes(request):
    message = 'Всего рецептов: '
    selected_ingredient_ids = request.POST.get('ingredients', '').split(',')
    difficulty = request.POST.get('difficulty', '')
    time = request.POST.get('time', '')
    fullHit = request.POST.get('coincidence')
    # if fullHit:
    #     print("true")
    # else:
    #     print("false")

    #  selected_ingredient_ids не пуст и не содержит пустых значений
    selected_ingredient_ids = [id for id in selected_ingredient_ids if id]

    recipes = Recipe.objects.all()
    percentsDict = []

    # for index, value in enumerate(recipes):
    #     recipes[index] = {'recipe' : value, 'percentage' : 100}


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
            # total_ingredients = recipe.ingredients.count()
            total_ingredients = selected_ingredient_ids.__len__()
            ingredients_in_recipe = recipe.ingredients.count()
            matching_ingredients = recipe.ingredients.filter(id__in=selected_ingredient_ids).count()
            # print(f"matching {recipe.title} - {matching_ingredients}")
            # print(f"total {recipe.title} - {total_ingredients}")
            # print(f"ingredients {recipe.title} - {ingredients_in_recipe}")
            percentage = (matching_ingredients / ingredients_in_recipe) * 100
            comparisonPercents = 100 if fullHit else 70
            if percentage >= comparisonPercents:
                # filtered_recipes.append({ 'recipe' : recipe, 'percentage' : percentage })
                filtered_recipes.append(recipe)
                percents = f"{int(percentage)}%"
                percentsDict.append({ recipe : percents })
                # print(percentsDict[0])
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