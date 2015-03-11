from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.
from translator.executables.nlp import translator


def create(request):
    return render(request, 'translator/create.html')


def translate(request):
    textlist = request.POST.getlist('text[]')
    print(textlist)
    # text = "The robot says 'Hi'"
    ret = ""
    i=1;
    for text in textlist:
        if text != "":
            ret += "%d.<div class='program-step'>%s</div>" % (i,translator.translate(text))
            i+=1

    return HttpResponse(ret)