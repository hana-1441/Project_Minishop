# Generated by Django 5.0 on 2024-01-23 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_cart_qty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='qty',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
