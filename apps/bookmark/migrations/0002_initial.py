# Generated by Django 5.1.2 on 2024-10-10 04:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
        ('bookmark', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='audiobookbookmark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_bookmarks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ebookbookmark',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_bookmarks', to='book.book'),
        ),
        migrations.AddField(
            model_name='ebookbookmark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_bookmarks', to=settings.AUTH_USER_MODEL),
        ),
    ]
