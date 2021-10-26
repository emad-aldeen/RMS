# Generated by Django 3.2.8 on 2021-10-26 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='point',
            name='cohort',
        ),
        migrations.AlterField(
            model_name='point',
            name='prize',
            field=models.CharField(blank=True, choices=[('WAIVE_LATE_SUBMISSION', 'WAIVE_LATE_SUBMISSION'), ('RANDOM_3D_ITEM', 'RANDOM_3D_ITEM'), ('RESUBMIT', 'RESUBMIT'), ('+1_MARK', '+1_MARK'), ('WAIVE_LATE_ATTENDANCE', 'WAIVE_LATE_ATTENDANCE'), ('DONATE', 'DONATE')], max_length=80),
        ),
    ]
