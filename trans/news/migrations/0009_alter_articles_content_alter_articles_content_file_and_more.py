# Generated by Django 4.0.4 on 2022-05-07 18:46

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_alter_articles_content_alter_articles_content_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True, verbose_name='Редактор'),
        ),
        migrations.AlterField(
            model_name='articles',
            name='content_file',
            field=models.FileField(blank=True, null=True, upload_to='media', verbose_name='Текстовый документ'),
        ),
        migrations.AlterField(
            model_name='articles',
            name='content_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на текстовый документ'),
        ),
        migrations.AlterField(
            model_name='articles',
            name='date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации'),
        ),
    ]