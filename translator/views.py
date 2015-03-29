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
    steps = []
    for text in textlist:
        if text == "":
            ret_dictionary[i] = "{}"
            steps.append({})
        else:
            result = translator.translate(text, i)
            ret_dictionary[i] = translator.get_json(result)
            steps.append(result)
        i += 1

    request.session['steps'] = steps
    ret = json.dumps(ret_dictionary)
    return HttpResponse(ret)


def csv(request):
    steps=request.session['steps'];
    csvfile = StringIO()
    for step in steps:
        if step != {}:
            translator.get_csv(step, csvfile)

    string = csvfile.getvalue()
    print(string)
    response = HttpResponse(csvfile.getvalue(), content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename=scenario.csv'
    response['Content-Length'] = csvfile.tell()
    return response