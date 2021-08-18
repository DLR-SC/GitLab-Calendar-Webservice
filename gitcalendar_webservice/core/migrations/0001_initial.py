# Generated by Django 3.2.6 on 2021-08-17 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GitLabAPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('gitlab_api_token', models.CharField(max_length=300)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CalendarConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config_name', models.CharField(max_length=20)),
                ('only_issues', models.BooleanField(verbose_name='Only Issues')),
                ('only_milestones', models.BooleanField(verbose_name='Only Milestones')),
                ('api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.gitlabapi')),
            ],
        ),
    ]
