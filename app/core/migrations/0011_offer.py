# Generated by Django 3.2.20 on 2023-08-01 16:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_accesstoken_expires_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price', models.PositiveIntegerField(max_length=10)),
                ('items_in_stock', models.PositiveIntegerField(max_length=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='core.product')),
            ],
        ),
    ]