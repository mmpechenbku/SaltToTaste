from django import forms
from .models import CommentRecipe, Recipe, RecipeStep, IngredientQuantity
from django.forms import modelformset_factory

class CommentCreateForm(forms.ModelForm):
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'cols': 30,
        'rows': 5,
        'placeholder': 'Комментарий',
        'class': 'form-control'
    }))

    class Meta:
        model = CommentRecipe
        fields = ('content',)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'difficulty', 'cookingTime', 'picture', 'ingredients']


class StepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = ['description', 'image']


class IngredientQuantityForm(forms.ModelForm):
    class Meta:
        model = IngredientQuantity
        fields = ['ingredient', 'quantity']

IngredientQuantityFormSet = modelformset_factory(IngredientQuantity, form=IngredientQuantityForm, extra=1)

class RecipeStepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = ['description', 'image']

StepFormSet = modelformset_factory(RecipeStep, form=RecipeStepForm, extra=1)