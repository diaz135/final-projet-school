# Generated by Django 2.2.12 on 2024-12-19 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0002_auto_20241219_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affectationmatiere',
            name='matiere',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructeurs', to='school.Matiere'),
        ),
        migrations.DeleteModel(
            name='Matiere',
        ),
    ]
