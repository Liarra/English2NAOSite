from translator.executables.nlp.components.execution import *
from translator.executables.nlp.components.moves.demo_moves import *
from translator.executables.nlp.encoders import encode2csv
from translator.executables.nlp.translation.ranker import TextBreaker
from translator.executables.nlp.components.robot_commands import *
from translator.executables.nlp.states import grammar

__author__ = 'NBUCHINA'


def translate(text, step_number=1, components_from_db=None):
    components = [say_command, wait_command,
                  wave, nod, handshake, stand, cry, crouch, dance,
                  button_press,
                  Sequence, Parallel, GoTo]

    if not components_from_db:
        components_from_db = []

    components.extend(components_from_db)

    text_ranker = TextBreaker(text)
    components_mapping = text_ranker.get_components(components)

    components_from_text = []

    for text, found_component in components_mapping:
        if found_component is not None:
            components_from_text.append(found_component)

    grammar.state_counter = step_number
    grammar.unrecognised_enabled = False
    components_from_text = grammar.transform(components_from_text)
    grammar.unite_condition_states(components_from_text)

    return components_from_text


def get_csv_file_with_header():
    return encode2csv.init_csv()


def get_csv(steps, csv_for_result):
    steps_list = grammar.get_new_list_with_keypress_states(steps)
    encode2csv.write_csv_from_steps(steps_list, csv_for_result)