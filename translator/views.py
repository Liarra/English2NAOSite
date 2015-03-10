from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.
from translator.executables.nlp import translator


def create(request):
    return render(request, 'translator/create.html')


def translate(request):
    text=request.POST['text']
    #text = "The robot says 'Hi'"
    return HttpResponse(str(translator.translate(text)))