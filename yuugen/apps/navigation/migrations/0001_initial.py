# Generated by Django 3.2 on 2022-10-05 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('ctag', models.CharField(max_length=254, unique=True, verbose_name='Catalog Tag')),
                ('cimg', models.ImageField(blank=True, max_length=254, upload_to='img', verbose_name='Catalog Image')),
                ('cslug', models.SlugField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ctag_creator', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ctag_editor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NewsLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='OperationTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('otag', models.CharField(max_length=254, unique=True, verbose_name='Operation Tag')),
                ('oimg', models.ImageField(blank=True, max_length=254, upload_to='img', verbose_name='Catalog Image')),
                ('oslug', models.SlugField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='otag_creator', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='otag_editor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ThemeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('ttag', models.CharField(max_length=254, unique=True, verbose_name='Theme Tag')),
                ('tslug', models.SlugField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ttag_creator', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ttag_editor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(max_length=254, upload_to='img', verbose_name='image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('SKU', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_sku', to='inventory.productdetail')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='image_creator', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='image_editor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('SKU', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_sku', to='inventory.productdetail')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_creator', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('ctag', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_catalog_tag', to='navigation.catalogtag')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_editor', to=settings.AUTH_USER_MODEL)),
                ('otag', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_operation_tag', to='navigation.operationtag')),
                ('ttag', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_theme_tag', to='navigation.themetag')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='FlatPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(db_index=True, max_length=100, verbose_name='URL')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('content', models.TextField(verbose_name='content')),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='page_creator', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='page_editor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Flat page',
                'verbose_name_plural': 'Flat pages',
                'ordering': ['url'],
            },
        ),
    ]
