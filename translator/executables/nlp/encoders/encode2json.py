from collections import OrderedDict
from translator.executables.nlp.substep import ConditionSubStep

__author__ = 'NBUCHINA'


def EncodeStepsArrayToJSON(steps):
    import json

    json_steps_array = []
    steps.sort(key=lambda x: float(x.ID), reverse=False)
    for step in steps:
        # print(SubStep.ID)

        step_data = {}
        if isinstance(step, ConditionSubStep):
            step_data["conditions"] = [str(x) for x in step.condition]

        step_data["actions"] = [str(x) for x in step.commands]
        step_data["nextID"] = step.next_ID
        step_data["stepID"] = step.ID

        json_steps_array.append(step_data)

    return json.dumps(json_steps_array)