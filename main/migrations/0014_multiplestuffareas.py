# Generated by Django 2.2 on 2019-04-15 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_area_stuff'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultipleStuffAreas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stuff', to='main.Area', verbose_name='Локация')),
                ('stuff', models.ManyToManyField(blank=True, related_name='stuff', to='main.Stuff', verbose_name='Оборудование')),
            ],
            options={
                'verbose_name': 'Оборудование и другое',
                'verbose_name_plural': 'Оборудование и другое',
            },
        ),
    ]