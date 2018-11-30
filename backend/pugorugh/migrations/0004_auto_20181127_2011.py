# Generated by Django 2.1.3 on 2018-11-28 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0003_auto_20181124_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='gender',
            field=models.CharField(choices=[('m', 'male'), ('f', 'female'), ('U', 'unknown')], max_length=2),
        ),
        migrations.AlterField(
            model_name='dog',
            name='image_filename',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='gender',
            field=models.CharField(choices=[('m', 'male'), ('f', 'female'), ('U', 'unknown')], max_length=2),
        ),
    ]