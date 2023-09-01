# Generated by Django 4.2.3 on 2023-08-29 11:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worshipKart', '0005_alter_productcategory_categoryimages'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='quantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worshipKart.products')),
            ],
        ),
        migrations.CreateModel(
            name='orders',
            fields=[
                ('orderId', models.AutoField(primary_key=True, serialize=False)),
                ('orderDate', models.DateField(default=datetime.date.today)),
                ('orderPrice', models.DecimalField(decimal_places=2, max_digits=15)),
                ('paymentMode', models.CharField(choices=[('IB', 'Internet Banking'), ('Wallet', 'Wallet'), ('UPI', 'UPI'), ('COD', 'Cash on Delivery')], max_length=100)),
                ('address', models.TextField()),
                ('products', models.ManyToManyField(through='worshipKart.OrderProduct', to='worshipKart.products')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worshipKart.usermaster')),
            ],
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worshipKart.orders'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worshipKart.products'),
        ),
    ]