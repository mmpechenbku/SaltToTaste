from django.urls import path, include
from .views import *

urlpatterns = [
    path('', search_recipes, name='search'),
    path('save_recipe/', SaveRecipeCreateView.as_view(), name='save_recipe'),
    path('api/ingredients/', IngredientSearchView.as_view(), name='ingredient-search'),
]