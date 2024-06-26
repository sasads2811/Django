# Generated by Django 4.2.13 on 2024-05-21 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScoreRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate', models.CharField(max_length=100)),
                ('score', models.FloatField()),
                ('scoring_date', models.DateField()),
                ('province', models.CharField(max_length=50)),
            ],
        ),
    ]
