# Generated by Django 3.1.2 on 2020-11-15 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('gender', models.CharField(default='male', max_length=10)),
                ('age', models.CharField(default='low', max_length=10)),
                ('movieType', models.TextField()),
                ('lang', models.TextField()),
                ('genre', models.TextField()),
                ('newUser', models.BooleanField(default=False)),
                ('dateJoined', models.DateField()),
            ],
        ),
    ]