# Generated by Django 3.2.8 on 2021-10-26 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211026_0304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='randomuser',
            name='username',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('ta', 'TA'), ('student', 'Student'), ('instructor', 'Instructor')], default='student', max_length=80),
        ),
    ]