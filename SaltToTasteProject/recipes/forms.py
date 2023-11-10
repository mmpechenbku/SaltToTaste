from django import forms
from .models import CommentRecipe, Recipe, RecipeStep

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
        fields = ['title', 'description', 'difficulty', 'cooking_time', 'image', 'ingredients']


class StepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = ['description', 'image']