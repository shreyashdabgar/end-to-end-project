# Generated by Django 5.1.4 on 2025-01-08 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shreyash_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='image',
            field=models.ImageField(upload_to='food/'),
        ),
    ]
