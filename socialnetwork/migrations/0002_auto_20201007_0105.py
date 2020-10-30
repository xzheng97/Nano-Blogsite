# Generated by Django 3.1.1 on 2020-10-07 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(default=None, related_name='_profile_following_+', to='socialnetwork.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='content_type',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_bio',
            field=models.CharField(default='hello, welcome to my profile!', max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_picture',
            field=models.FileField(blank=True, default=None, upload_to=''),
        ),
    ]