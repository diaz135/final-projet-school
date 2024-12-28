# Generated by Django 2.2.12 on 2024-12-26 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20241225_2310'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={},
        ),
        migrations.RenameField(
            model_name='question',
            old_name='timeframe',
            new_name='timeframe_duration',
        ),
        migrations.RemoveField(
            model_name='question',
            name='date_update',
        ),
        migrations.RemoveField(
            model_name='question',
            name='point',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question',
        ),
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='question',
            name='typequestion',
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(blank=True, choices=[('qcm', 'QCM'), ('question-reponse', 'Question-Réponse')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='timeframe_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='timeframe_unit',
            field=models.CharField(blank=True, choices=[('hour', 'Heures'), ('minute', 'Minutes')], max_length=10, null=True),
        ),
    ]