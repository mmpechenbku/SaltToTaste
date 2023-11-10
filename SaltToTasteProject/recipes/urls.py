from django.urls import path, include
from .views import *

urlpatterns = [
    path('', search_recipes, name='search'),
    path('collections/', collections, name='collections'),
    path('save_recipe/', SaveRecipeCreateView.as_view(), name='save_recipe'),
    path('recipe/<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment_create_view'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('add_recipe/', add_recipe, name='add_recipe'),
    path('api/ingredients/', IngredientSearchView.as_view(), name='ingredient-search'),
]