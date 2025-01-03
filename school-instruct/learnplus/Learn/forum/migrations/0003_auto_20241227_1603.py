# Generated by Django 2.2.12 on 2024-12-27 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20200501_1319'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reponse',
            options={'ordering': ['-date_add'], 'verbose_name': 'Reponse', 'verbose_name_plural': 'Reponses'},
        ),
        migrations.AlterModelOptions(
            name='sujet',
            options={'ordering': ['-date_add'], 'verbose_name': 'Sujet', 'verbose_name_plural': 'Sujets'},
        ),
        migrations.RenameField(
            model_name='reponse',
            old_name='reponse',
            new_name='contenu',
        ),
        migrations.RemoveField(
            model_name='reponse',
            name='slug',
        ),
    ]
