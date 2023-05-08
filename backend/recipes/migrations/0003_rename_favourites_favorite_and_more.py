# Generated by Django 4.2 on 2023-05-08 14:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Favourites',
            new_name='Favorite',
        ),
        migrations.RenameModel(
            old_name='ShoppingList',
            new_name='ShoppingCart',
        ),
        migrations.AlterModelOptions(
            name='favorite',
            options={'default_related_name': 'favorite', 'verbose_name': 'избранное', 'verbose_name_plural': 'избранное'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'default_related_name': 'shopping_cart', 'verbose_name': 'список покупок', 'verbose_name_plural': 'список покупок'},
        ),
    ]
