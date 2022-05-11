from .models import Articles
from django.forms import ModelForm, TextInput, FileInput, DateTimeInput, CharField, BooleanField, Form
from ckeditor.widgets import CKEditorWidget


class ArticlesForm(ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'media', 'date']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название конспекта',
            }),
            'media': FileInput(attrs={
                'class': 'form-control'

            }),
            'date': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата загрузки'
            })
        }


class ArticleEditForm(Form):
    content = CharField(widget=CKEditorWidget(), initial='Здесь появится обработанный текст', label='Редактор текста')
    save_to_drive = BooleanField(label='Сохранить на диск?', required=False)
