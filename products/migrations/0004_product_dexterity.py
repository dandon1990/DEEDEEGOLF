# Generated by Django 3.2 on 2023-01-29 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20230128_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='dexterity',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]