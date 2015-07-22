from itertools import cycle
import json
import pickle

from django.shortcuts import render
from django.http import HttpResponse

from translator.executables.nlp import commons
from translator.executables.nlp.components.component import UnrecognisedComponent
from translator.executables.nlp.components.moves.demo_moves import *
from translator.executables.nlp.translation import translator
from translator.executables.nlp.components.robot_commands import *
from translator.models import *


def create(request):
    return render(request, 'translator/create.html')


def edit(request, program_id):
    scenario = Scenario.objects.get(id=program_id)
    states = pickle.loads(scenario.pickled_formal_description)
    saved_textual_descriptions = scenario.step_set.all()
    descriptions = []
    for saved_description in saved_textual_descriptions:
        descriptions.append([saved_description.step_name, saved_description.step_description])

    context = {'states_list': states, 'descriptions_list': saved_textual_descriptions}
    request.session['states'] = states
    request.session['step_descriptions'] = descriptions

    return render(request, 'translator/create.html', context)


def translate(request):
    text_list = request.POST.getlist('text[]')
    header_list = request.POST.getlist('headers[]')
    i = 1

    states = []
    step_descriptions = []

    components=load_actions_from_db()+load_conditions_from_db()

    header_cycle = cycle(header_list)
    for text in text_list:
        step_descriptions.append([next(header_cycle), text])

        if text == "":
            states.append({})
        else:
            result = translator.translate(text, i, components)
            states.append(result)
        i += 1

    request.session['states'] = states
    request.session['step_descriptions'] = step_descriptions

    context = {'states_list': states}
    return render(request, 'translator/formal_description.html', context)


def save_program(request):
    text_list = request.POST.getlist('text[]')
    header_list = request.POST.getlist('headers[]')
    step_descriptions = []

    header_cycle = cycle(header_list)
    for text in text_list:
        step_descriptions.append([next(header_cycle), text])

    states = request.session['states']

    pickled_states = pickle.dumps(states)

    new_program = Scenario()
    new_program.pickled_formal_description = pickled_states
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
    states = request.session['states']

    #remove unrecognised parts, if any
    for states_for_step in states:
        for state in states_for_step:
            for command in state.commands:
                if isinstance(command, UnrecognisedComponent):
                    state.commands.remove(command)
                    if len(state.commands) == 0:
                        states_for_step.remove(state)

    csv_file = translator.get_csv_file_with_header_and_first_state(states[0])
    for states_for_step in states:
        if states_for_step != {}:
            translator.write_csv(states_for_step, csv_file)

    response = HttpResponse(csv_file.getvalue(), content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename=scenario.csv'
    response['Content-Length'] = csv_file.tell()
    csv_file.close()
    return response


def state_editor(request):
    states = request.session['states']
    state_id = request.POST['substep_id'].strip()

    state_to_display = None
    for states_for_step in states:
        for state in states_for_step:
            id = None
            if hasattr(state, "uID"):
                id = state.uID
            else:
                id = state.ID

            if id == state_id:
                state_to_display = state

    context = {'state': state_to_display}
    return render(request, 'translator/state_editor.html', context)


def get_components_list(request):
    components = load_actions_from_db()
    conditions = load_conditions_from_db()

    if request.POST["components_type"] == "components":
        context = {'components_list': components}
    else:
        context = {'components_list': conditions}

    return render(request, "translator/components_list.html", context)


def get_component_params(request):
    states = request.session['states']
    state_id = request.POST['substep_id'].strip()

    action_index = None
    condition_index = None

    if 'substep_action_index' in request.POST:
        action_index = int(request.POST['substep_action_index'].strip())
    elif 'substep_condition_index' in request.POST:
        condition_index = int(request.POST['substep_condition_index'].strip())

    action = None
    for states_for_step in states:
        for state in states_for_step:
            id = None
            if hasattr(state, "uID"):
                id = state.uID
            else:
                id = state.ID
            if id == state_id:
                if action_index:
                    action = state.commands[action_index - 1]
                elif condition_index:
                    action = state.condition[condition_index - 1]

    context = {'component': action}
    return render(request, "translator/component_properties.html", context)


def get_component_class_params(request):
    class_name = request.POST['class_name'].strip()
    class_class = commons.class_for_name("translator.executables.nlp.components.robot_commands", class_name)

    context = {'class': class_class}
    return render(request, "translator/component_properties.html", context)


def remove_state(request):
    states = request.session['states']
    state_id_for_removal = request.POST['substep_id'].strip()

    for states_for_step in states:
        for state in states_for_step:
            id = None
            if hasattr(state, "uID"):
                id = state.uID
            else:
                id = state.ID
            if id == state_id_for_removal:
                states_for_step.remove(state)

    request.session['states'] = states
    return HttpResponse("OK")


def update_state(request):
    from translator.executables.nlp.states import program_editor

    # TODO: Make a good JSON here.
    state_id = request.POST['substep_id'].strip()
    actions_to_add = json.loads(request.POST.get('actions_to_add'))
    conditions_to_add = json.loads(request.POST.get('conditions_to_add'))
    actions_to_remove = json.loads(request.POST.get('actions_to_remove'))
    conditions_to_remove = json.loads(request.POST.get('conditions_to_remove'))
    change_actions = json.loads(request.POST.get('change_actions'))
    change_conditions = json.loads(request.POST.get('change_actions'))
    change_next_id = json.loads(request.POST.get('change_next_id'))

    request.session["states"] = program_editor.update_state(request.session["states"], state_id,
                                                           actions_to_add, conditions_to_add,
                                                           actions_to_remove, conditions_to_remove,
                                                           change_actions, change_conditions,
                                                           change_next_id)
    states = request.session["states"]
    context = {'states_list': states}
    return render(request, 'translator/formal_description.html', context)


def load_actions_from_db():
    components = [say_command, wait_command,
                  wave, nod, handshake, stand, cry, crouch, dance]

    atomic_components = AtomicActionComponent.objects.all()
    user_components = UserActionComponent.objects.all()

    return components

def load_conditions_from_db():
    conditions=[button_press]

    atomic_components = AtomicActionComponent.objects.all()
    user_components = UserActionComponent.objects.all()

    return conditions

def load_user_selected_actions_from_db():
    pass

def load_user_selected_conditions_from_db():
    pass
