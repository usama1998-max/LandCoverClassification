# Generated by Django 4.2.5 on 2023-11-04 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detect_map', '0009_alter_imagesimilarity_img_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagesimilarity',
            name='img_similarity_score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]
