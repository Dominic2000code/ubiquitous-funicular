# Generated by Django 4.2.4 on 2023-08-25 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_post_views_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='privacy_level',
            field=models.CharField(choices=[('public', 'Public'), ('friends_only', 'Friends Only'), ('private', 'Private')], default='public', max_length=20),
        ),
    ]
