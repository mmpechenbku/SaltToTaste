from django.urls import path, include
from .views import *


recipes_urls = [
    path('', search_recipes, name='search'),
    path('collections/', selections, name='collections'),
    path('favorites/', favorites, name='favorites'),
    path('collections/<int:pk>/', CollectionDetailView.as_view(), name='collections-detail'),

    path('collections-detail/', collections_detail, name='collections-detail'),


    path('save_recipe/', SaveRecipeCreateView.as_view(), name='save_recipe'),
    path('save_collection', SaveSelectionCreateView.as_view(), name='save_collection'),
    path('like_comment/', LikeCommentCreateView.as_view(), name='like_comment'),
    path('recipe/<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment_create_view'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    # path('recipe/<int:pk>', recipe_detail, name='recipe_detail'),
    path('recipe_add/', add_recipe, name='add_recipe'),
    # path('test_add_recipe/', test_add_recipe, name='add_recipe'),
    path('create_selection/', create_selection, name='create_selection'),
    path('api/ingredients/', IngredientSearchView.as_view(), name='ingredient-search'),
]

urlpatterns = [
    path('', index, name='home'),
    path('search/', include(recipes_urls)),

]

