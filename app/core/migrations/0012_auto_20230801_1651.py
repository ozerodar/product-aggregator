# Generated by Django 3.2.20 on 2023-08-01 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='items_in_stock',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='offer',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]
