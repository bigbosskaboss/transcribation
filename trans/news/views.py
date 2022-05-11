import os

from django.shortcuts import render, redirect
from django.conf import settings
from .models import Articles
from .forms import ArticlesForm, ArticleEditForm

from htmldocx import HtmlToDocx
import mammoth as mam

from .transcribation import Transcrib
from .utils.load_to_drive import upload_file

transcrib = Transcrib()
html_parser = HtmlToDocx()


# Список конспектов
def news_home(request):

    if request.method == 'POST':
        if request.POST.get("article-edit"):
            return redirect('edit', pk=int(request.POST.get('article-edit')))
        elif request.POST.get("article-delete"):
            article = Articles.objects.filter(pk=int(request.POST.get('article-delete')))[0]
            os.remove(str(settings.DOCS_ROOT / f"{article.title}_{article.pk}.docx"))
            os.remove(str(settings.MEDIA_ROOT / str(article.media)))
            article.delete()

    news = Articles.objects.order_by('-date')
    articles = [{'text': mam.convert_to_html(open(settings.DOCS_ROOT / f"{article.title}_{article.pk}.docx",
                                                  'rb')).value,
                 'pk': article.pk,
                 'media': article.media,
                 'doc_url': article.doc_url,
                 'title': article.title} for article in news]

    return render(request, 'news/news_home.html', {'articles': articles})


# Создание конспекта
def create(request):
    data = {
        'load_form': ArticlesForm(),
        'edit_form': ArticleEditForm(),
        'error': '',
        'text': '',
        'metadata': '',
        'form_checked': False
    }
    if request.method == 'POST':

        if request.POST.get("handle-file"):
            data['load_form'] = ArticlesForm(request.POST, request.FILES)

            if data['load_form'].is_valid():

                data['load_form'].save()
                data['form_checked'] = True
                data['media_path'] = Articles.objects.last().media
                # data['edit_form'].fields['content'].initial = "Текст для тестов"
                transcrib.set_wf(str(data['media_path']))
                data['edit_form'].fields['content'].initial = "<br><br>".join(transcrib.handle())

                return render(request, 'news/create.html', data)
            else:
                data['error'] = 'Форма заполнена неверно'

        elif request.POST.get("save-article"):
            # !!!Исправить получение id
            article = Articles.objects.last()
            id = article.id
            title = Articles.objects.filter(id=id)[0].title
            d = html_parser.parse_html_string(request.POST['content'])
            d.save(settings.DOCS_ROOT / f'{title}_{id}.docx')

            if request.POST.get('save_to_drive', '') == 'on':
                doc_url = upload_file(settings.DOCS_ROOT, f'{title}_{id}.docx')
                article.doc_url = doc_url
                article.save()

            return redirect('news_home')

    return render(request, 'news/create.html', data)


# Редактирование конспекта
def edit(request, pk):
    data = {'edit_form': ArticleEditForm(),
            'article': Articles.objects.filter(pk=pk)[0]}
    text = mam.convert_to_html(open(settings.DOCS_ROOT /
                                    f'{data["article"].title}_{data["article"].pk}.docx', 'rb')).value
    data['media_path'] = data['article'].media
    data['edit_form'].fields['content'].initial = text

    if request.method == "POST":

        article = Articles.objects.filter(pk=pk)[0]
        title = article.title
        d = html_parser.parse_html_string(request.POST['content'])
        doc_path = settings.DOCS_ROOT / f'{title}_{pk}.docx'
        d.save(doc_path)

        if request.POST.get('save_to_drive', '') == 'on':
            doc_url = upload_file(settings.DOCS_ROOT, f'{title}_{pk}.docx')
            article.doc_url = doc_url
            article.save()

        return redirect('news_home')

    return render(request, 'news/edit.html', data)
