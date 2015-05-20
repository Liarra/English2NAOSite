from functools import reduce
import json
import sys
from translator.executables.nlp.substep import ConditionSubStep, SubStep

__author__ = 'NBUCHINA'


def update_substep(steps_list, substep_id,
                   actions_to_add=None, conditions_to_add=None,
                   actions_to_remove=None, conditions_to_remove=None,
                   change_actions=None, change_conditions=None):
    if not conditions_to_remove:
        conditions_to_remove = []
    if not change_actions:
        change_actions = []
    if not actions_to_add:
        actions_to_add = []
    if not actions_to_remove:
        actions_to_remove = []
    if not conditions_to_add:
        conditions_to_add = []
    if not change_conditions:
        change_conditions = []
    new_steps = steps_list
    for step in new_steps:
        for substep in step:
            id = -1
            if (hasattr(substep, 'uID')):
                id = substep.uID
            else:
                id = substep.ID

            if id == substep_id:
                # First, change stuff
                for i in range(0, len(change_actions)):
                    action_params = json.loads(change_actions[i])
                    substep.commands[i].load_params(action_params)

                for i in range(0, len(change_conditions)):
                    condition_params = json.loads(change_conditions[i])
                    substep.condition[i].load_params(condition_params)

                # Then remove stuff
                for action_index in actions_to_remove:
                    del substep.commands[action_index]

                for condition_index in conditions_to_remove:
                    del substep.condition[condition_index]
                    if len(substep.condition) == 0:
                        substep.__class__ = SubStep

                # Finally, add new stuff
                for action in actions_to_add:
                    action_params = json.loads(action)
                    action_class_name = action_params["class"]
                    # action_class = globals()[action_class_name]
                    action_class = class_for_name("translator.executables.nlp.components.robot_commands",action_class_name)
                    action_instance = action_class()
                    action_instance.load_params(action_params)
                    substep.commands.append(action_instance)

                for condition in conditions_to_add:
                    condition_params = json.loads(condition)
                    condition_class_name = condition_params["class"]
                    condition_class = globals()[condition_class_name]
                    condition_instance = condition_class()
                    condition_instance.load_params(condition_params)

                    if not hasattr(substep, 'conditions'):
                        substep.conditions = []
                        substep.__class__ = ConditionSubStep
                    substep.conditions.append(condition_instance)

    return new_steps


import importlib

def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c