from wsgiref.util import FileWrapper
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import json
from io import StringIO
import pickle
from translator.executables.nlp import translator
from translator.models import RobotProgram


def create(request):
    return render(request, 'translator/create.html')


# def edit(request, id):
# program=RobotProgram.

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
    request.session['text_description'] = textlist

    ret = json.dumps(ret_dictionary)
    # return HttpResponse(ret)

    context = {'steps_list': steps}
    return render(request, 'translator/program.html', context)


def save_program(request):
    steps = request.session['steps']
    description = request.session['text_description']

    pickled_steps = pickle.dumps(steps)
    pickled_description = pickle.dumps(description)

    new_program = RobotProgram()
    new_program.text_description = description
    new_program.pickled_formal_description = steps

    new_program.save()

    return view_scenarios(request)


def view_scenarios(request):
    scenarios_list = RobotProgram.objects.all()
    context = {'scenarios_list': scenarios_list}

    return render(request, 'translator/list.html', context)


def csv(request):
    steps = request.session['steps']
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