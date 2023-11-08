from django.urls import path, include
from .views import *

urlpatterns = [
    path('', search_recipes, name='search'),
    path('recipe', recipe_detail, name='recipe_detail'),
    path('api/ingredients/', IngredientSearchView.as_view(), name='ingredient-search'),
]