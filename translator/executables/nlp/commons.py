import importlib
import json
from translator.executables.nlp.components.robot_commands import Action
from translator.models import AtomicActionComponent, Component, AtomicConditionComponent

__author__ = 'NBUCHINA'


def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


def get_component_from_model(model):
    if not isinstance(model, Component):
        raise ValueError("model must be a Component")
    if hasattr(model, "actioncomponent"):
        model = model.actioncomponent
        if hasattr(model, "atomicactioncomponent"):
            model = model.atomicactioncomponent

    if hasattr(model, "conditioncomponent"):
        model = model.conditioncomponent
        if hasattr(model, "atomicconditioncomponent"):
            model = model.atomicconditioncomponent

    if isinstance(model, AtomicActionComponent) or isinstance(model, AtomicConditionComponent):
        component_class_name = model.component_class
        component_class = class_for_name("translator.executables.nlp.components.robot_commands", component_class_name)

        new_component = component_class()
        if len(model.regex) > 0:
            new_component.regexp = model.regex
        if len(model.name) > 0:
            new_component.name = model.name
        if len(model.summary) > 0:
            new_component.summary = model.summary
        if len(model.command) > 0:
            new_component.command = model.command

        chars_to_remove = ["\r", "\n", "\b", "\f", "\t"]
        dd = {ord(c): None for c in chars_to_remove}
        new_params_string = model.params.translate(dd)
        new_component.load_params(json.loads(new_params_string))
        new_component.tags.update(model.tags.names())

        new_component.ref_id = model.id

        return new_component


def get_model_from_atomic_action(action):
    model = AtomicActionComponent()
    model.component_class = action.__class__.__name__
    model.regex = action.regexp
    model.name = action.name
    model.summary = action.summary
    model.command = action.command

    json_params_string = json.dumps(action.params)
    model.params = json_params_string

    return model


def get_model_from_atomic_condition(condition):
    model = AtomicConditionComponent()
    model.component_class = condition.__class__.__name__
    model.regex = condition.regexp
    model.name = condition.name
    model.summary = condition.summary
    model.command = condition.command

    json_params_string = json.dumps(condition.params)
    model.params = json_params_string

    return model


def get_all_atomic_action_components():
    models = AtomicActionComponent.objects.all()
    ret = []
    for model in models:
        ret.append(get_component_from_model(model))

    return ret


def get_all_atomic_condition_components():
    models = AtomicConditionComponent.objects.all()
    ret = []
    for model in models:
        ret.append(get_component_from_model(model))

    return ret


def get_component_by_ref_id(ref_id):
    return get_component_from_model(Component.objects.get(id=ref_id))
