# Generated by Django 3.0.5 on 2020-05-04 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_image_show_video'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playlist',
            options={'ordering': ['last_updated_date']},
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='location',
        ),
        migrations.AlterField(
            model_name='show',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
