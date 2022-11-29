# Generated by Django 3.2 on 2022-11-29 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='alt_text',
            field=models.CharField(blank=True, max_length=255, verbose_name='alternate text'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='img',
            field=models.ImageField(max_length=254, upload_to='', verbose_name='image'),
        ),
    ]
