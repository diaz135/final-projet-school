# Generated by Django 2.2.8 on 2020-04-20 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='filiere',
        ),
        migrations.AlterField(
            model_name='student',
            name='classe',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='student_classe',
                to='school.Classe'),
        ),
    ]
