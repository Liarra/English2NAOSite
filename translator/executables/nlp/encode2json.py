from collections import OrderedDict
from translator.executables.nlp.step import cstep

__author__ = 'NBUCHINA'


def EncodeStepsArrayToJSON(steps):
    import json

    json_dict = OrderedDict()
    steps.sort(key=lambda x: float(x.state_ID), reverse=False)
    for step in steps:
        print(step.state_ID)
        stepID = step.state_ID

        step_data = {}
        if isinstance(step, cstep):
            step_data["conditions"] = [str(x) for x in step.condition]

        step_data["actions"] = [str(x) for x in step.commands]
        step_data["nextID"] = step.next_state_ID

        json_dict[stepID] = step_data

    return json.dumps(json_dict)