# Generated by Django 5.0 on 2023-12-27 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_vacancy_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='vacancy_photos/'),
        ),
    ]
