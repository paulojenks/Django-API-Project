# Generated by Django 2.1.3 on 2018-12-03 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0006_auto_20181128_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpref',
            name='age',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='gender',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='size',
            field=models.CharField(max_length=20),
        ),
    ]