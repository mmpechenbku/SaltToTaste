# Generated by Django 4.2.6 on 2023-12-13 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_customuser_birth_date'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='customuser',
        #     name='birth_date',
        # ),
        migrations.AddField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
    ]
