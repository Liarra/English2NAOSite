from itertools import cycle
import json
import pickle

from django.shortcuts import render
from django.http import HttpResponse

from translator.executables.nlp import commons
from translator.executables.nlp.translation import translator
from translator.executables.nlp.components.robot_commands import button_press
from translator.models import *


def create(request):
    return render(request, 'translator/create.html')


def edit(request, program_id):
    scenario = Scenario.objects.get(id=program_id)
    steps = pickle.loads(scenario.pickled_formal_description)
    saved_textual_descriptions = scenario.step_set.all()
    descriptions = []
    for saved_description in saved_textual_descriptions:
        descriptions.append([saved_description.step_name, saved_description.step_description])

    context = {'steps_list': steps, 'descriptions_list': saved_textual_descriptions}
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
    return render(request, 'translator/formal_description.html', context)


def save_program(request):
    textlist = request.POST.getlist('text[]')
    headerlist = request.POST.getlist('headers[]')
    step_descriptions = []

    header_cycle = cycle(headerlist)
    for text in textlist:
        step_descriptions.append([next(header_cycle), text])

    steps = request.session['steps']

    pickled_steps = pickle.dumps(steps)

    new_program = Scenario()
    new_program.pickled_formal_description = pickled_steps
    new_program.save()

    for heading, text in step_descriptions:
        new_step = Step()
        new_step.step_description = text
        new_step.step_name = heading
        new_step.scenario = new_program
        new_step.save()

    return view_scenarios(request)


def view_scenarios(request):
    scenarios_list = Scenario.objects.all()
    context = {'scenarios_list': scenarios_list}

    return render(request, 'translator/list.html', context)


def csv(request):
    steps = request.session['steps']
    csvfile = translator.get_csv_file_with_header()
    for step in steps:
        if step != {}:
            translator.get_csv(step, csvfile)

    string = csvfile.getvalue()
    print(string)
    response = HttpResponse(csvfile.getvalue(), content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename=scenario.csv'
    response['Content-Length'] = csvfile.tell()
    csvfile.close()
    return response


def substep_editor(request):
    steps = request.session['steps']
    step_id = request.POST['substep_id'].strip()

    step_for_display = None
    for step in steps:
        for substep in step:
            id = None
            if hasattr(substep, "uID"):
                id = substep.uID
            else:
                id = substep.ID

            if id == step_id:
                step_for_display = substep

    context = {'substep': step_for_display}
    return render(request, 'translator/state_editor.html', context)


def substep_editor_components_list(request):
    from translator.executables.nlp.components.robot_commands import say_command, wait_command
    from translator.executables.nlp.components.moves.demo_moves import wave, nod, handshake

    components = [say_command, wait_command,
                  wave, nod, handshake]

    conditions = [button_press]

    if request.POST["components_type"] == "components":
        context = {'components_list': components}
    else:
        context = {'components_list': conditions}

    return render(request, "translator/components_list.html", context)


def substep_editor_params(request):
    steps = request.session['steps']
    step_id = request.POST['substep_id'].strip()

    action_index = None
    condition_index = None

    if 'substep_action_index' in request.POST:
        action_index = int(request.POST['substep_action_index'].strip())
    elif 'substep_condition_index' in request.POST:
        condition_index = int(request.POST['substep_condition_index'].strip())

    action = None
    for step in steps:
        for substep in step:
            id = None
            if hasattr(substep, "uID"):
                id = substep.uID
            else:
                id = substep.ID
            if id == step_id:
                if action_index:
                    action = substep.commands[action_index - 1]
                elif condition_index:
                    action = substep.condition[condition_index - 1]

    context = {'component': action}
    return render(request, "translator/component_properties.html", context)


def substep_editor_class_params(request):
    class_name = request.POST['class_name'].strip()
    class_class = commons.class_for_name("translator.executables.nlp.components.robot_commands", class_name)

    context = {'class': class_class}
    return render(request, "translator/component_properties.html", context)


def remove_substep(request):
    steps = request.session['steps']
    step_id_for_removal = request.POST['substep_id'].strip()

    for step in steps:
        for substep in step:
            id = None
            if hasattr(substep, "uID"):
                id = substep.uID
            else:
                id = substep.ID
            if id == step_id_for_removal:
                step.remove(substep)

    request.session['steps'] = steps
    return HttpResponse("OK")


def update_substep(request):
    from translator.executables.nlp.states import program_editor

    # TODO: Make a good JSON here.
    step_id = request.POST['substep_id'].strip()
    actions_to_add = json.loads(request.POST.get('actions_to_add'))
    conditions_to_add = json.loads(request.POST.get('conditions_to_add'))
    actions_to_remove = json.loads(request.POST.get('actions_to_remove'))
    conditions_to_remove = json.loads(request.POST.get('conditions_to_remove'))
    change_actions = json.loads(request.POST.get('change_actions'))
    change_conditions = json.loads(request.POST.get('change_actions'))

    request.session["steps"] = program_editor.update_state(request.session["steps"], step_id,
                                                           actions_to_add, conditions_to_add,
                                                           actions_to_remove, conditions_to_remove,
                                                           change_actions, change_conditions)
    steps = request.session["steps"]
    context = {'steps_list': steps}
    return render(request, 'translator/formal_description.html', context)


def load_components_from_db():
    atomic_components = AtomicActionComponent.objects.all()
    # TODO: Rather select components from the user's library
    user_components = UserActionComponent.objects.all()
    pass
