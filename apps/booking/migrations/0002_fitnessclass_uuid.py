# Generated by Django 4.2.22 on 2025-06-09 11:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitnessclass',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
