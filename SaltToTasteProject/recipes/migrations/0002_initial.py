# Generated by Django 4.2.6 on 2023-12-14 02:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='selection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='saveselection',
            name='selection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saving_selection', to='recipes.selection', verbose_name='Подборка'),
        ),
        migrations.AddField(
            model_name='saveselection',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='saverecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saving', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='saverecipe',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='recipestep',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='ingredients', to='recipes.ingredient'),
        ),
        migrations.AddField(
            model_name='likecomment',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_comment', to='recipes.commentrecipe', verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='likecomment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='ingredientquantity',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AddField(
            model_name='ingredientquantity',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='commentrecipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария'),
        ),
        migrations.AddField(
            model_name='commentrecipe',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='recipes.commentrecipe', verbose_name='Родительский комментарий'),
        ),
        migrations.AddField(
            model_name='commentrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddIndex(
            model_name='saveselection',
            index=models.Index(fields=['-time_create'], name='recipes_sav_time_cr_2a486c_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='saveselection',
            unique_together={('selection', 'user')},
        ),
        migrations.AddIndex(
            model_name='saverecipe',
            index=models.Index(fields=['-time_create'], name='recipes_sav_time_cr_73bca6_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='saverecipe',
            unique_together={('recipe', 'user')},
        ),
        migrations.AddIndex(
            model_name='likecomment',
            index=models.Index(fields=['-time_create'], name='recipes_lik_time_cr_05d208_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='likecomment',
            unique_together={('comment', 'user')},
        ),
        migrations.AddIndex(
            model_name='commentrecipe',
            index=models.Index(fields=['-time_create', 'time_update', 'status', 'parent'], name='app_comment_time_cr_0c0ec5_idx'),
        ),
    ]
