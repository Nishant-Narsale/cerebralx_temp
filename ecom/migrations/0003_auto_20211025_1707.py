# Generated by Django 3.2.7 on 2021-10-25 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0002_customer_order_orderitem_shippingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='optional_address',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='address',
            field=models.TextField(max_length=1000),
        ),
    ]
