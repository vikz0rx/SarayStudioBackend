# Generated by Django 2.2 on 2019-04-15 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20190415_1438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='stuff',
        ),
    ]
