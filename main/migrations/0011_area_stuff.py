# Generated by Django 2.2 on 2019-04-15 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_multipleimageareas'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='stuff',
            field=models.ManyToManyField(blank=True, null=True, related_name='stuff', to='main.Stuff', verbose_name='Оборудование'),
        ),
    ]
