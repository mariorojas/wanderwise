# Generated by Django 5.1.4 on 2024-12-06 21:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(max_length=30, unique=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('content', models.TextField(max_length=10000)),
                ('author', models.CharField(max_length=30)),
                ('external_url', models.URLField()),
                ('created_utc', models.BigIntegerField(blank=True, null=True)),
                ('mention_type', models.CharField(choices=[('fb', 'Facebook'), ('li', 'LinkedIn'), ('rd', 'Reddit'), ('tw', 'X (Twitter)')], default='other', max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=3000)),
                ('url', models.URLField(blank=True, null=True)),
                ('num_of_mentions', models.IntegerField(default=0)),
                ('num_of_replies', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=200)),
                ('num_of_mentions', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keywords', to='core.campaign')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('keyword', 'campaign'), name='unique_keyword_campaign')],
            },
        ),
    ]
