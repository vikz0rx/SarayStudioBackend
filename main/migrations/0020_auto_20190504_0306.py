# Generated by Django 2.2 on 2019-05-03 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_photographs_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='makeup',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='makeup', verbose_name='Фотография'),
        ),
        migrations.AlterField(
            model_name='multipleimagemakeup',
            name='image',
            field=models.ImageField(upload_to='makeup', verbose_name='Фотография'),
        ),
    ]