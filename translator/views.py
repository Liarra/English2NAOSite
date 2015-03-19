from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import json

# Create your views here.
from translator.executables.nlp import translator


def create(request):
    return render(request, 'translator/create.html')


def translate(request):
    textlist = request.POST.getlist('text[]')
    # print(textlist)
    # text = "The robot says 'Hi'"
    i = 1

    ret_dictionary = {}
    for text in textlist:
        if text == "":
            ret_dictionary[i] = "{}"
        else:
            ret_dictionary[i] = translator.translate(text, i)
        i += 1

    print(i)

    ret = json.dumps(ret_dictionary)
    return HttpResponse(ret)