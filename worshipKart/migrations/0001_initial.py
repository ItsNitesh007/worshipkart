# Generated by Django 4.2.3 on 2023-08-19 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='productCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productCategoryId', models.CharField(default='', max_length=30)),
                ('productCategoryName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='products',
            fields=[
                ('productId', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('productName', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('description', models.TextField()),
                ('productimage', models.ImageField(blank=True, null=True, upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='productSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productSubCategoryId', models.CharField(default='', max_length=30)),
                ('productSubCategoryName', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='userMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=30)),
                ('lastName', models.CharField(max_length=30)),
                ('contact', models.IntegerField(unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=15)),
                ('newsletter', models.BooleanField()),
                ('userType', models.CharField(choices=[('Buyer', 'Buyer'), ('Admin', 'Admin')], default='Buyer', max_length=10)),
            ],
        ),
    ]
