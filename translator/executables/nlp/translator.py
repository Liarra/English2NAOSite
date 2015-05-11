from translator.executables.nlp.components.component import *
from translator.executables.nlp.components.execution import *
from translator.executables.nlp.components.moves.demo_moves import *
from translator.executables.nlp.encoders import encode2csv
from translator.executables.nlp.encoders import encode2json
from translator.executables.nlp.ranker import text_breaker
from translator.executables.nlp.components.robot_commands import *
from translator.executables.nlp import grammar

__author__ = 'NBUCHINA'


def translate(text, step_number=1, components_from_db=[]):
    components = [say_command, wait_command,
                  wave, nod, handshake,
                  button_press,
                  sequence, parallel, goto]

    components.extend(components_from_db)

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


def get_json(steps):
    return encode2json.EncodeStepsArrayToJSON(steps)


def get_csv(steps, csv_for_result):
    steps_list = grammar.get_new_list_with_ksteps(steps)
    encode2csv.writeCSVFromSteps(steps_list, csv_for_result)