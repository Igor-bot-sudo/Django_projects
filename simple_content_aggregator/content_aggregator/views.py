import os
import feedparser
import re
import httpx
import requests
from bs4 import BeautifulSoup
from django.http import FileResponse
from django.shortcuts import render
from simple_content_aggregator.settings import BASE_DIR


def index(request):
    if os.path.exists('content_aggregator/templates/show_page.html'):
        os.remove('content_aggregator/templates/show_page.html')
    if os.path.exists('content_aggregator/templates/doc.pdf'):
        os.remove('content_aggregator/templates/doc.pdf')
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def get_content(url, out_list):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_='lh-small-article-card article-card__small')
    for k in range(len(quotes)):
        s = str(quotes[k])
        result = re.search(r'<div class="lh-small-article-card__title"'
                           r' data-jest="title">(.*?)</div>', s)
        title = result.group(1)
        result = re.search(
            r'<a aria-label=".*?" class="lh-small-article-card__link"'
            r' data-jest="link" href="(.*?)" name=".*?"></a>',
            s)
        if 'https://' in result.group(1):
            link = result.group(1)
        else:
            link = f'https://lifehacker.ru{result.group(1)}'
        result = re.search(r'<img.*?class="lh-small-article-card__cover".*?src="(.*?)".*?/>', s)
        img = result.group(1)
        content = {'title': title, 'link': link, 'img': img}
        out_list.append(content)


def pdf_export(request):
    with open('content_aggregator/templates/show_page.html', 'r', encoding="utf-8") as fp:
        ss = fp.read()
    ss = ss.replace(f'<div style="text-align: right; margin-right: 50px;">\
    <a href="/pdf/">Export to PDF</a></div><br><br>', '')
    with open('content_aggregator/templates/show_page.html', 'w', encoding="utf-8") as fp:
        fp.write(ss)
    cmd = f'wkhtmltopdf.exe --enable-local-file-access \
    "{BASE_DIR}/content_aggregator/templates/show_page.html" \
    "{BASE_DIR}/content_aggregator/templates/doc.pdf"'
    os.system(cmd)
    return FileResponse(open(f'{BASE_DIR}/content_aggregator/templates/doc.pdf', 'rb'),
                        content_type='application/pdf')


def show_page(request):
    url = request.GET.get('hr')
    title = request.GET.get('t')
    type_ = request.GET.get('type')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    if type_ == 'BS4':
        quote = soup.find('main', class_='single-article__content')
    elif type_ == 'RSS':
        # quote = soup.find('div', class_='article__body')
        quote = soup.find('div', class_='page page-article')

    ss = f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">\
    <meta name="viewport" content="width=device-width, initial-scale=1.0">\
    <link href="static/css/style.css" rel="stylesheet" type="text/css" />\
    <link rel="icon" href="static/img/favicon.svg" type="image/svg+xml">\
    <title>{title}</title></head><body>\
    <div style="text-align: right; margin-right: 50px;">\
    <a href="/pdf/">Export to PDF</a></div><br><br>{str(quote)}</body></html>'
    with open('content_aggregator/templates/show_page.html', 'w', encoding="utf-8") as fp:
        fp.write(ss)

    return render(request, 'show_page.html')

    # return render(request, 'show_page.html', context={'title': title, 'body': str(quote),
    #               'export': '<div style="text-align: right; margin-right: 50px;">\
    #                         <a href="/pdf/">Export to PDF</a></div><br><br>'})


def bs4_view(request):
    url = 'https://lifehacker.ru/top/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('a', class_='lh-the-paginator__cell')
    pages = max([int(x.text) for x in quotes])
    out_list = []
    get_content(url, out_list)  # first page
    for i in range(2, pages + 1):  # next pages
        t_url = url + f'week/?page={i}'
        get_content(t_url, out_list)
    return render(request, 'index.html', context={'message': out_list, 'type': 'BS4'})


def rss_view(request):
    httpx_client = httpx.Client()
    rss_link = 'https://www.vedomosti.ru/rss/rubric/technology'
    try:
        response = httpx_client.get(rss_link)
    except:
        pass
    feed = feedparser.parse(response.text)
    out_list = []
    for entry in feed.entries[::-1]:
        content = {'title': entry['title'], 'link': entry['link'], 'img': 'N/A'}
        if entry.enclosures:
            for enclosure in entry.enclosures:
                if enclosure['type'] == 'image/jpeg':
                    content['img'] = enclosure['href']
                    break
        out_list.append(content)
    return render(request, 'index.html', context={'message': out_list, 'type': 'RSS'})
