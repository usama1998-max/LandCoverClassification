# Generated by Django 4.2.5 on 2023-10-27 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detect_map', '0005_delete_imagesegment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageSegment',
            fields=[
                ('img_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='detect_map.images')),
                ('land', models.FileField(default='', upload_to='user_imgs_segment')),
                ('water', models.FileField(default='', upload_to='user_imgs_segment')),
            ],
        ),
    ]
