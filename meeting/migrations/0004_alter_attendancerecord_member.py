# Generated by Django 3.2.13 on 2023-04-30 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0003_attendancerecord_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancerecord',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='meeting.attendee'),
        ),
    ]
