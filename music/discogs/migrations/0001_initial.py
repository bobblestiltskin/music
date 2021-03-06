# Generated by Django 2.2.17 on 2020-11-04 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artists',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Formats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('format', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Labels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catalogue_number', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('released', models.DateTimeField(verbose_name='date released')),
                ('release_id', models.CharField(max_length=200)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discogs.Artists')),
                ('format', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discogs.Formats')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discogs.Labels')),
            ],
        ),
    ]
