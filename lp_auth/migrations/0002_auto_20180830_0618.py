# Generated by Django 2.1 on 2018-08-30 06:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('lp_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]