from itertools import cycle
from io import StringIO
import pickle

from django.shortcuts import render
from django.http import HttpResponse

from translator.executables.nlp import translator
from translator.models import *


def create(request):
    return render(request, 'translator/create.html')


def edit(request, program_id):
    program = RobotProgram.objects.get(id=program_id)
    steps = pickle.loads(program.pickled_formal_description)
    saved_steps_descriptions = program.programstep_set.all()
    descriptions = []
    for saved_description in saved_steps_descriptions:
        descriptions.append([saved_description.step_name, saved_description.step_description])

    context = {'steps_list': steps, 'descriptions_list': saved_steps_descriptions}
    request.session['steps'] = steps
    request.session['step_descriptions'] = descriptions

    return render(request, 'translator/create.html', context)


def translate(request):
    textlist = request.POST.getlist('text[]')
    headerlist = request.POST.getlist('headers[]')
    i = 1

    # ret_dictionary = {}
    steps = []
    step_descriptions = []

    header_cycle = cycle(headerlist)
    for text in textlist:
        step_descriptions.append([next(header_cycle), text])

        if text == "":
            steps.append({})
        else:
            result = translator.translate(text, i)
            steps.append(result)
        i += 1

    request.session['steps'] = steps
    request.session['step_descriptions'] = step_descriptions

    context = {'steps_list': steps}
    return render(request, 'translator/program.html', context)


def save_program(request):
    textlist = request.POST.getlist('text[]')
    headerlist = request.POST.getlist('headers[]')
    step_descriptions = []

    header_cycle = cycle(headerlist)
    for text in textlist:
        step_descriptions.append([next(header_cycle), text])

    steps = request.session['steps']

    pickled_steps = pickle.dumps(steps)

    new_program = RobotProgram()
    new_program.pickled_formal_description = pickled_steps
    new_program.save()

    for heading, text in step_descriptions:
        new_step = ProgramStep()
        new_step.step_description = text
        new_step.step_name = heading
        new_step.program = new_program
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


def substep_editor(request):
    steps = request.session['steps']
    step_id = request.POST['substep_id'].strip()

    step_for_display = None
    for step in steps:
        for substep in step:
            if substep.ID == step_id:
                step_for_display = substep

    context = {'substep': step_for_display}
    return render(request, 'translator/substep_editor.html', context)


def substep_editor_components_list(request):
    from translator.executables.nlp.components.robot_commands import say_command, wait_command
    from translator.executables.nlp.components.moves.demo_moves import wave, nod, handshake

    components = [say_command, wait_command,
                  wave, nod, handshake]

    context = {'components_list': components}
    return render(request, "translator/components_list.html", context)

def substep_editor_params(request):
    steps = request.session['steps']
    step_id = request.POST['substep_id'].strip()
    action_index = int(request.POST['substep_action_index'].strip())

    action=None
    for step in steps:
        for substep in step:
            if substep.ID == step_id:
                action=substep.commands[action_index-1]

    context = {'component': action}
    return render(request, "translator/component_properties.html", context)


def remove_substep(request):
    steps = request.session['steps']
    step_id_for_removal = request.POST['substep_id'].strip()

    for step in steps:
        for substep in step:
            if substep.ID == step_id_for_removal:
                step.remove(substep)

    request.session['steps'] = steps
    return HttpResponse("OK")
    # TODO: Change SubStep id, add command etc


def load_components_from_db():
    atomic_components = AtomicActionComponent.objects.all()
    # TODO: Rather select components from the user's library
    user_components = UserActionComponent.objects.all()
    pass
