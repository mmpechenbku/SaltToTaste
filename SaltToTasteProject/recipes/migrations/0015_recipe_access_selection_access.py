# Generated by Django 4.2.6 on 2023-12-01 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_alter_recipe_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='access',
            field=models.CharField(choices=[('public', 'Общедоступный'), ('private', 'Личный')], default='private', max_length=10, verbose_name='Доступ'),
        ),
        migrations.AddField(
            model_name='selection',
            name='access',
            field=models.CharField(choices=[('public', 'Общедоступный'), ('private', 'Личный')], default='private', max_length=10, verbose_name='Доступ'),
        ),
    ]