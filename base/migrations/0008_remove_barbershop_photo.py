# Generated by Django 4.2.2 on 2023-09-22 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_barbershop_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barbershop',
            name='photo',
        ),
    ]
