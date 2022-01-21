# Generated by Django 3.1.13 on 2022-01-12 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_management', '0003_auto_20220103_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sprints', to='project_management.project'),
        ),
        migrations.AlterField(
            model_name='task',
            name='dev',
            field=models.ForeignKey(limit_choices_to={'user_type': 'Dev'}, on_delete=django.db.models.deletion.CASCADE, related_name='my_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='sprint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='project_management.sprint'),
        ),
    ]
