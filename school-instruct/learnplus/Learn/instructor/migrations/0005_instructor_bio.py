# Generated by Django 2.2.8 on 2020-04-30 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0004_instructor_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='bio',
            field=models.TextField(default='Votre bio'),
        ),
    ]
