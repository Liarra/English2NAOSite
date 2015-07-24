import importlib
import json
from translator.models import AtomicActionComponent, Component

__author__ = 'NBUCHINA'


def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


def getComponentFromModel(model):
    if not isinstance(model, Component):
        raise ValueError("model must be a Component")

    if isinstance(model, AtomicActionComponent):
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
        new_component.tags.extend(model.tags.names())

        new_component.ref_id = model.id

        return new_component


def getAllAtomicActionComponents():
    models = AtomicActionComponent.objects.all()
    ret = []
    for model in models:
        ret.append(getComponentFromModel(model))

    return ret


def get_component_by_ref_id(ref_id):
    return getComponentFromModel(AtomicActionComponent.objects.get(id=ref_id))