# Generated by Django 2.2 on 2019-04-14 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_stuff_stuffkind'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stuffkind',
            old_name='title',
            new_name='name',
        ),
    ]