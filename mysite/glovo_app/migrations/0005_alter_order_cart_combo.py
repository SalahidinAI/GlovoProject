# Generated by Django 5.1.5 on 2025-01-20 06:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glovo_app', '0004_alter_order_cart_combo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cart_combo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='glovo_app.cartcombo'),
        ),
    ]
