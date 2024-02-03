# package imports
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import json

# local imports
from .models import *
from . import html_generators as _html

def home(request):
    return render(request, "home.html")

class QuotesView(View):
    queryset = Quote.objects 

    def get(self, request, *args, **kwargs):
        _id = request.GET.get('quote_id')
        _author = request.GET.get('author')
        _queryset = self.queryset.all()

        if _id is not None:
            _queryset = _queryset.filter(id=int(_id))

        if _author:
            _queryset = _queryset.filter(author__iexact=_author)

        _html_contents = ["<ul>"]
        for q in _queryset:
            _html_contents.append(_html.quote_list_item(q.id, q.quote, q.author))
        _html_contents.append("</ul>")

        return HttpResponse(''.join(_html_contents))

    def post(self, request, *args, **kwargs):
        _quote = request.POST.get('quote-input')
        _author = request.POST.get('author-input')
        
        # validations
        if not (_quote and _author):
            return HttpResponse("Bad request payload!", status=400)

        # update the db with the new data
        q = self.queryset.create(quote=_quote, author=_author)

        return HttpResponse(_html.quote_list_item(q.id, q.quote, q.author), status=201)

def delete_quote(request, *args, **kwargs):
    _id = kwargs['quote_id']
    _rows_deleted = Quote.objects.filter(id=_id).delete()
    if _rows_deleted:
        return HttpResponse("", status=200)
    else:
        return HttpResponse("", status=500)


def quotes(request):
    _quote = Quote.objects.all()
    _quotes_list = []
    for q in _quote:
        _quotes_list.append(q.complete_quote)

    return HttpResponse(json.dumps(_quotes_list))


def quote_by_id(request, quote_id):
    _quote = Quote.objects\
        .filter(id=quote_id)\
        .first()
    if _quote is not None:
        return HttpResponse(_quote.complete_quote)
    else:
        return HttpResponse(f"No quote with id={quote_id} found!", status=404)


def quote_by_author(request, author):
    _quote = Quote.objects\
        .filter(author__iexact=author)
    
    _quote_by_author = []
    for q in _quote:
        _quote_by_author.append(q.complete_quote)

    if _quote_by_author:
        return HttpResponse(json.dumps(_quote_by_author))
    else:
        return HttpResponse(f"No quote by author \"{author}\" found!", status=404)
