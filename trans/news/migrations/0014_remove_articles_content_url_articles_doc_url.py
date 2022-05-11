# Generated by Django 4.0.4 on 2022-05-08 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_alter_articles_content_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articles',
            name='content_url',
        ),
        migrations.AddField(
            model_name='articles',
            name='doc_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на текстовый документ'),
        ),
    ]
