import django_filters
from .models import *

class RecipeFilter(django_filters.FilterSet):

    CHOICE_DIFFICULTY = (
        ('Сложно', 'Сложно'),
    )

    difficulty = django_filters.MultipleChoiceFilter(choices=CHOICE_DIFFICULTY, lookup_expr="icontains")
    cookingTime = django_filters.TimeFilter(label="Время приготовления")

    class Meta:
        model = Recipe
        fields = ['difficulty', 'cookingTime']