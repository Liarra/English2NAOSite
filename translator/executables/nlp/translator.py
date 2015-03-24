from translator.executables.nlp.components.component import *
from translator.executables.nlp.components.execution import *
from translator.executables.nlp.encoders import encode2csv
from translator.executables.nlp.encoders import encode2json
from translator.executables.nlp.ranker import text_breaker
from translator.executables.nlp.components.robot_commands import *
from translator.executables.nlp import grammar

__author__ = 'NBUCHINA'


def translate(text, step_number=1):
    components = [say_command, wait_command, move_command,
                  button_press,
                  sequence, parallel, goto]

    ranker1 = text_breaker(text)
    components_mapping = ranker1.map_components_to_text(components)

    result = []
    components_from_text = []

    for text, component in components_mapping:
        if component is not None:
            components_from_text.append(component)

    grammar.step_counter = step_number
    grammar.unrecognised_enabled = False
    components_from_text = grammar.go_through(components_from_text)
    grammar.unite_csteps(components_from_text)

    return components_from_text


def get_json(text, step_number=1):
    components = translate(text, step_number)
    return encode2json.EncodeStepsArrayToJSON(components)


def get_csv(text, csv_for_result, step_number=1):
    components = translate(text, step_number)
    steps_list = grammar.get_new_list_with_ksteps(components)

    encode2csv.writeCSVFromSteps(steps_list, csv_for_result)