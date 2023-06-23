# Generated by Django 4.2.2 on 2023-06-23 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0007_gratitudeentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='WinEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Win Entry')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='win_entries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Win Entries',
                'ordering': ['created_on'],
            },
        ),
    ]
