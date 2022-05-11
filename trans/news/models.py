from django.db import models


class Articles(models.Model):
    title = models.TextField('Название')
    media = models.FileField('Аудиозапись', upload_to="media")
    date = models.DateTimeField('Дата публикации', null=True, blank=True)
    doc_url = models.URLField('Ссылка на текстовый документ', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Конспект'
        verbose_name_plural = 'Конспекты'
