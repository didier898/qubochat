# Generated by Django 4.2.5 on 2023-09-20 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='pin',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
