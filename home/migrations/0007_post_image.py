# Generated by Django 4.2.3 on 2023-09-18 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_post_options_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/home/imges'),
        ),
    ]