from django.urls import path, include
from .views import *

urlpatterns = [
    path('', search_recipes, name='search'),
    path('api/ingredients/', IngredientSearchView.as_view(), name='ingredient-search'),
]