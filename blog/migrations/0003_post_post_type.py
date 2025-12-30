# Generated migration for adding post_type field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_episode_number_season_post_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(
                choices=[('blog', 'Blog'), ('journal', 'Journal')],
                default='blog',
                max_length=20
            ),
        ),
    ]
