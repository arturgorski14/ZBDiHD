# Generated by Django 2.0 on 2020-06-15 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('studio', models.CharField(max_length=300)),
                ('platform', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=5000)),
                ('release_date', models.DateField()),
                ('average_rating', models.FloatField(default=0)),
                ('image', models.URLField(default=None, null=True)),
            ],
        ),
    ]
