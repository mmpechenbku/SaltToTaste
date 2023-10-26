from django.db import models

from SaltToTasteProject.SaltToTasteProject import settings

# Create your models here.

# CHOICE_DIFFICULTY = (
#     ('Сложно', 'Сложно'),
# )

# CHOICE_CATEGORY = (
#     ('Овощи', 'Овощи'),
# )

class Recipe(models.Model):
    class Difficulty(models.TextChoices):
        HARD = "Сложно"
        MEDIUM = "Средняя"
        EASY = "Легко"
    # picture = models.ManyToManyField('Picture', blank=True)
    picture = models.ImageField(upload_to='images/recipes_pictures', verbose_name='Фото')
    title = models.CharField(max_length=255, verbose_name='Название')
    ingredients = models.ManyToManyField('Ingredient', related_name='ingredients')
    description = models.TextField(verbose_name="Описание приготовления")
    # difficulty = models.CharField(max_length=50, choices=CHOICE_DIFFICULTY, verbose_name='Сложность')
    difficulty = models.CharField(max_length=50, choices=Difficulty.choices, verbose_name='Сложность')
    # cookingTime = models.IntegerField(verbose_name='Время приготовления')
    cookingTime = models.TimeField(verbose_name="Время приготовления")
    likesCount = models.IntegerField(verbose_name='Количество лайков')
    commentsCount = models.IntegerField(verbose_name='Количество комментариев')

class Ingredient(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    class Category(models.TextChoices):
        FRUITS = "Фрукт"
        VEGETABLES = "Овощи"
        MEAT = "Мясо"
    category = models.CharField(max_length=150, choices=Category.choices, verbose_name='Категория')

# class RecipeIngredients(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
#     ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredients')

# class RecipeLikes(models.Model):
#     recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, verbose_name='Рецепт', related_name='like_recipe')
#     user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='like_user')
#     time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
#     ip_address = models.GenericIPAddressField(verbose_name='IP Адрес')
#
#     class Meta:
#         unique_together = ('recipe', 'ip_address')
#         ordering = ('-time_create',)
#         indexes = [models.Index(fields=['-time_create', 'value'])]
#         verbose_name = 'Лайк'
#         verbose_name_plural = 'Лайки'
#
#     def __str__(self):
#         return self.recipe.title

# class RecipeLikes(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='like_user')
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт', related_name='like_recipe')
#
# class RecipeComment(models.Model):
#     comment = models.TextField(verbose_name='Комментарий')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='comment_user')
#     selection = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт', related_name='comment_recipe')

class Selection(models.Model):
    picture = models.ImageField(upload_to='images/selection_pictures', verbose_name='Фото')
    title = models.CharField(max_length=255, verbose_name='Название')
    recipes = models.ManyToManyField(Recipe, related_name='recipes')

# class SelectionRecipes(models.Model):
#     selection = models.ForeignKey(Selection, on_delete=models.CASCADE, verbose_name='Подборка', related_name='selection')
#     recipe = models.ForeignKey(Selection, on_delete=models.CASCADE, verbose_name='Рецепт', related_name='recipe')

# class SelectionLikes(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='like_user')
#     selection = models.ForeignKey(Selection, on_delete=models.CASCADE, verbose_name='Подборка', related_name='like_selection')
#
# class SelectionComment(models.Model):
#     comment = models.TextField(verbose_name='Комментарий')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='comment_user')
#     selection = models.ForeignKey(Selection, on_delete=models.CASCADE, verbose_name='Подборка', related_name='comment_selection')

# class Picture(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='pictures')
#     image = models.ImageField(upload_to='images/recipes_pictures', verbose_name='Фото')
#     def __str__(self):
#         return str(self.image)
#
#     class Meta:
#         verbose_name = 'Фото'
#         verbose_name_plural = 'Фотографии'