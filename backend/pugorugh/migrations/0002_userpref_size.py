# Generated by Django 2.1.3 on 2018-11-25 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpref',
            name='size',
            field=models.CharField(choices=[('s', 'small'), ('m', 'medium'), ('l', 'large'), ('xl', 'x-large'), ('U', 'unknown')], default='s', max_length=2),
            preserve_default=False,
        ),
    ]
