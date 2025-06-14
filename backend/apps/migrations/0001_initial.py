# Generated by Django 5.0.6 on 2025-05-18 04:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'categoría',
                'verbose_name_plural': 'categorías',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(blank=True, null=True)),
                ('complete', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'orden',
                'verbose_name_plural': 'ordenes',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=200, null=True)),
                ('descripcion', models.TextField(blank=True, max_length=1000, null=True)),
                ('precio', models.IntegerField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('cantidad', models.IntegerField(default=0)),
                ('stock', models.IntegerField(default=0)),
                ('estado', models.IntegerField(default=0)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.categoria')),
            ],
            options={
                'verbose_name': 'producto',
                'verbose_name_plural': 'productos',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.order')),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.producto')),
            ],
            options={
                'verbose_name': 'item de orden',
                'verbose_name_plural': 'items de orden',
            },
        ),
    ]
