from itertools import cycle
from wsgiref.util import FileWrapper
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import json
from io import StringIO
import pickle
from translator.executables.nlp import translator
from translator.models import RobotProgram, ProgramStep


def create(request):
    return render(request, 'translator/create.html')


def edit(request, program_id):
    program = RobotProgram.objects.get(id=program_id)
    steps = pickle.loads(program.pickled_formal_description)
    descriptions = program.programstep_set.all()

    context = {'steps_list': steps, 'descriptions_list': descriptions}
    return render(request, 'translator/create.html', context)


def translate(request):
    textlist = request.POST.getlist('text[]')
    headerlist = request.POST.getlist('headers[]')
    i = 1

    ret_dictionary = {}
    steps = []
    step_descriptions = []

    header_cycle = cycle(headerlist)
    for text in textlist:
        step_descriptions.append([next(header_cycle), text])

        if text == "":
            steps.append({})
        else:
            result = translator.translate(text, i)
            ret_dictionary[i] = translator.get_json(result)
            steps.append(result)
        i += 1

    request.session['steps'] = steps
    request.session['step_descriptions'] = step_descriptions

    context = {'steps_list': steps}
    return render(request, 'translator/program.html', context)


def save_program(request):
    steps = request.session['steps']
    description = request.session['step_descriptions']

    pickled_steps = pickle.dumps(steps)

    new_program = RobotProgram()
    new_program.pickled_formal_description = pickled_steps
    new_program.save()

    for heading, text in description:
        new_step = ProgramStep()
        new_step.step_description = text
        new_step.step_name = heading
        new_step.program=new_program
        new_step.save()

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