# Generated by Django 2.2 on 2019-04-15 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_area_stuff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='stuff',
            field=models.ManyToManyField(blank=True, related_name='stuff', to='main.Stuff', verbose_name='Оборудование'),
        ),
    ]
