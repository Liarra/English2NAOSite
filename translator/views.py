from wsgiref.util import FileWrapper
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import json
from io import StringIO
from translator.executables.nlp import translator


def create(request):
    return render(request, 'translator/create.html')


def translate(request):
    textlist = request.POST.getlist('text[]')
    i = 1

    ret_dictionary = {}
    for text in textlist:
        if text == "":
            ret_dictionary[i] = "{}"
        else:
            ret_dictionary[i] = translator.get_json(text, i)
        i += 1

    print(i)

    ret = json.dumps(ret_dictionary)
    return HttpResponse(ret)


def csv(request):
    textlist = request.POST.getlist('text[]')
    i = 1

    csvfile = StringIO()
    for text in textlist:
        if text != "":
            translator.get_csv(text, csvfile, i)
        i += 1

    string = csvfile.getvalue()
    print(string)
    response = HttpResponse(csvfile.getvalue(), content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename=scenario.csv'
    response['Content-Length'] = csvfile.tell()
    return response