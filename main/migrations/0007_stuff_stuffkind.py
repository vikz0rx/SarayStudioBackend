# Generated by Django 2.2 on 2019-04-14 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20190411_0141'),
    ]

    operations = [
        migrations.CreateModel(
            name='StuffKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория оборудования',
                'verbose_name_plural': 'Категории оборудования',
            },
        ),
        migrations.CreateModel(
            name='Stuff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('cost', models.PositiveSmallIntegerField(verbose_name='Стоимость')),
                ('rent_cost', models.PositiveSmallIntegerField(default=0, verbose_name='Стоимость аренды')),
                ('number', models.PositiveSmallIntegerField(default=1, verbose_name='Количество')),
                ('image', models.ImageField(upload_to='stuff', verbose_name='Изображение')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kind', to='main.StuffKind', verbose_name='Категория оборудования')),
            ],
            options={
                'verbose_name': 'Оборудование и другое',
                'verbose_name_plural': 'Оборудование и другое',
            },
        ),
    ]
