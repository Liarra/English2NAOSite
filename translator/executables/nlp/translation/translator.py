from translator.executables.nlp.components.component import IgnoredComponent
from translator.executables.nlp.components.execution import *
from translator.executables.nlp.encoders import encode2csv
from translator.executables.nlp.translation.ranker import TextBreaker
from translator.executables.nlp.states import grammar

__author__ = 'NBUCHINA'


def translate(text, step_number=1, components_from_db=None):
    components = [Sequence(), Parallel(), GoTo(),
                  IgnoredComponent()]

    if not components_from_db:
        components_from_db = []

    components.extend(components_from_db)

    text_ranker = TextBreaker(text)
    components_mapping = text_ranker.get_components(components)

    components_from_text = []

    for text, found_component in components_mapping:
        if found_component is not None:
            components_from_text.append(found_component)

    grammar.state_counter = step_number*1000
    grammar.unrecognised_enabled = False
    components_from_text = grammar.transform(components_from_text)
    grammar.unite_condition_states(components_from_text)
    components_from_text.sort(key=lambda x: x.ID, reverse=False)

    return components_from_text


def get_csv_file_with_header_and_first_state(first_states):
    csv_for_result= encode2csv.init_csv()
    states_list = grammar.get_new_list_with_keypress_states(first_states)
    encode2csv.write_first_csv_line(states_list, csv_for_result)

    return csv_for_result

def write_csv(states, csv_for_result):
    states_list = grammar.get_new_list_with_keypress_states(states)

    #  existing_ids = []
    #
    # for states_for_step in states:
    #     for state in states_for_step:
    #         existing_ids.append(state.ID)

    encode2csv.write_csv_from_states(states_list, csv_for_result)