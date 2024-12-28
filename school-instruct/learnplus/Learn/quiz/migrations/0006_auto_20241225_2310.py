# Generated by Django 2.2.12 on 2024-12-25 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20241225_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='question', name='timeframe', field=models.IntegerField(
                blank=True, null=True), ), migrations.AddField(
            model_name='question', name='timeframe_unit', field=models.CharField(
                blank=True, choices=[
                    ('hours', 'Heures'), ('minutes', 'Minutes')], max_length=10, null=True), ), ]