# Generated by Django 4.2.1 on 2023-05-31 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_blog', '0010_profile_fb_url_profile_instagram_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='header_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/header/'),
        ),
    ]
