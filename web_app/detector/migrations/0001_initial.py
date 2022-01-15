# Generated by Django 4.0.1 on 2022-01-15 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='detector/static/detector/videos')),
            ],
        ),
        migrations.CreateModel(
            name='Instances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_frame', models.IntegerField()),
                ('last_frame', models.IntegerField()),
                ('track_number', models.IntegerField()),
                ('class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detector.classes')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detector.videos')),
            ],
        ),
    ]