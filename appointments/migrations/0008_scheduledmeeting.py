# Generated by Django 5.0.6 on 2024-06-05 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0007_alter_meeting_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledMeeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('time', models.TimeField()),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
            ],
        ),
    ]