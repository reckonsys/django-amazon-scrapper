# Generated by Django 3.0.6 on 2020-05-11 17:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asin',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=5000)),
                ('price', models.FloatField(default=0.0)),
                ('qna_count', models.IntegerField(default=0)),
                ('rating', models.FloatField(default=0.0)),
                ('rating_count', models.IntegerField(default=0)),
                ('region', models.PositiveSmallIntegerField(choices=[(14, 'Arab Emirates'), (1, 'Australia'), (2, 'Brazil'), (3, 'China'), (5, 'Germany'), (12, 'Spain'), (4, 'France'), (6, 'India'), (7, 'Italy'), (8, 'Japan'), (9, 'Mexico'), (10, 'Netherland'), (11, 'Singapore'), (13, 'Turkey'), (15, 'United Kingdom'), (16, 'United States')], default=16)),
                ('status', models.PositiveSmallIntegerField(choices=[(2, 'Invalid'), (1, 'Newly Added'), (3, 'Valid')], default=1)),
                ('asin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='scrapper.Asin')),
            ],
            options={
                'unique_together': {('asin', 'region')},
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Scrape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(4, 'Created'), (3, 'Failed'), (2, 'Scrapping'), (5, 'Updated'), (1, 'Waiting')], default=1)),
                ('message', models.CharField(max_length=200)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scrapes', to='scrapper.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('rating', models.IntegerField(default=0)),
                ('text', models.TextField()),
                ('title', models.CharField(max_length=500)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='scrapper.Product')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='scrapper.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='scrapper.Product')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='scrapper.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='scrapper.Profile')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='scrapper.Question')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
