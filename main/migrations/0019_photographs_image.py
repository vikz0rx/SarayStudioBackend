# Generated by Django 2.2 on 2019-05-03 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_makeup_multipleimagemakeup'),
    ]

    operations = [
        migrations.AddField(
            model_name='photographs',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photograph', verbose_name='Фотография'),
        ),
    ]
