import json

from translator.executables.nlp.commons import class_for_name
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
                    action_params = change_actions[i]
                    substep.commands[i].load_params(action_params)

                for i in range(0, len(change_conditions)):
                    if not hasattr(substep, 'condition'): break
                    condition_params = change_conditions[i]
                    substep.condition[i].load_params(condition_params)

                # Then remove stuff
                for action_index in actions_to_remove:
                    del substep.commands[action_index]

                for condition_index in conditions_to_remove:
                    if not hasattr(substep, 'condition'): break
                    del substep.condition[condition_index]
                    if len(substep.condition) == 0:
                        substep.__class__ = SubStep

                # Finally, add new stuff
                for action in actions_to_add:
                    action_params = action
                    action_class_name = action_params["class"]
                    # action_class = globals()[action_class_name]
                    action_class = class_for_name("translator.executables.nlp.components.robot_commands",
                                                  action_class_name)
                    action_instance = action_class()
                    action_instance.load_params(action_params["params"])
                    substep.commands.append(action_instance)

                for condition in conditions_to_add:
                    condition_params = condition
                    condition_class_name = condition_params["class"]
                    condition_class = class_for_name("translator.executables.nlp.components.robot_commands",
                                                     condition_class_name)
                    condition_instance = condition_class()
                    condition_instance.load_params(condition_params["params"])

                    if not hasattr(substep, 'condition'):
                        substep.condition = []
                    substep.__class__ = ConditionSubStep
                    substep.condition.append(condition_instance)

    return new_steps
