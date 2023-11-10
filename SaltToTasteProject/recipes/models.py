from django.contrib.auth import get_user_model
from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

from SaltToTasteProject import settings

# Create your models here.

# CHOICE_DIFFICULTY = (
#     ('Сложно', 'Сложно'),
# )

# CHOICE_CATEGORY = (
#     ('Овощи', 'Овощи'),
# )

User = get_user_model()


class Recipe(models.Model):
    class RecipeManager(models.Manager):
        # def all(self):
        #     return self.get_queryset().select_related('author').prefetch_related('saveCount')

        def detail(self):
            return self.get_queryset()\
                .select_related('author')\
                .prefetch_related('comments', 'recipe_comments_author', 'ingredients', 'saving')

    class Difficulty(models.TextChoices):
        HARD = "Сложно"
        MEDIUM = "Средняя"
        EASY = "Легко"

    # picture = models.ManyToManyField('Picture', blank=True)
    picture = models.ImageField(upload_to='images/recipes_pictures', blank=True, null=True, verbose_name='Фото')
    title = models.CharField(max_length=255, verbose_name='Название')
    ingredients = models.ManyToManyField('Ingredient', related_name='ingredients')
    description = models.TextField(verbose_name="Описание приготовления")
    # difficulty = models.CharField(max_length=50, choices=CHOICE_DIFFICULTY, verbose_name='Сложность')
    difficulty = models.CharField(max_length=50, choices=Difficulty.choices, verbose_name='Сложность')
    # cookingTime = models.IntegerField(verbose_name='Время приготовления')
    cookingTime = models.TimeField(verbose_name="Время приготовления")
    # saveCount = models.IntegerField(default=0, verbose_name='Количество лайков')
    commentsCount = models.IntegerField(default=0, verbose_name='Количество комментариев')

    objects = RecipeManager()

    def get_sum_save(self):
        # return sum([1 for save in self.saving.all()])
        return self.saving.count()

    def get_sum_comments(self):
        return self.comments.count()

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')

    class Category(models.TextChoices):
        FRUITS = "Фрукт"
        VEGETABLES = "Овощи"
        MEAT = "Мясо"

    category = models.CharField(max_length=150, choices=Category.choices, verbose_name='Категория')

    def __str__(self):
        return self.name


class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт', related_name='steps')
    image = models.ImageField(upload_to='images/recipes_pictures/steps', blank=True, null=True, verbose_name='Фото шага')
    description = models.TextField(max_length=3000, verbose_name='Описание шага')
    step_number = models.IntegerField(verbose_name='Номер шага')


class SaveRecipe(models.Model):
    recipe = models.ForeignKey(to=Recipe, verbose_name='Рецепт', on_delete=models.CASCADE, related_name='saving')
    user = models.ForeignKey(to=User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)

    # ip_address = models.GenericIPAddressField(verbose_name='IP Адрес')

    class Meta:
        unique_together = ('recipe', 'user')
        ordering = ('-time_create',)
        indexes = [models.Index(fields=['-time_create'])]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return self.recipe.title


class Selection(models.Model):
    picture = models.ImageField(upload_to='images/selection_pictures', verbose_name='Фото')
    title = models.CharField(max_length=255, verbose_name='Название')
    recipes = models.ManyToManyField(Recipe, related_name='recipes')


class CommentRecipe(MPTTModel):
    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', related_name='recipe_comments_author')
    content = models.TextField(verbose_name='Текст комментария', max_length=3000)
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    status = models.CharField(choices=STATUS_OPTIONS, default='draft', verbose_name='Статус комментария', max_length=10)
    parent = TreeForeignKey('self', verbose_name='Родительский комментарий', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class MTTMeta:
        order_insertion_by = ('-time_create',)

    class Meta:
        db_table = 'app_comments'
        indexes = [models.Index(fields=['-time_create', 'time_update', 'status', 'parent'])]
        ordering = ['-time_create']
        verbose_name = 'Комментарий рецепта'
        verbose_name_plural = 'Комментарии рецептов'

    def __str__(self):
        return f'{self.author}:{self.content}'



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
