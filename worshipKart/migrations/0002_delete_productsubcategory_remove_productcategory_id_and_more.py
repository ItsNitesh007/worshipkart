# Generated by Django 4.2.3 on 2023-08-19 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worshipKart', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='productSubCategory',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='id',
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='productCategoryId',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]