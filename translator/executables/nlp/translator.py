from translator.executables.nlp.components.component import *
from translator.executables.nlp.components.execution import *
from translator.executables.nlp.encoders import encode2csv
from translator.executables.nlp.encoders import encode2json
from translator.executables.nlp.ranker import text_breaker
from translator.executables.nlp.components.robot_commands import *

__author__ = 'NBUCHINA'



def translate(text, step_number=1):
    components = [say_command, wait_command,move_command,
                  button_press,
                  sequence, parallel, goto]

    ranker1 = text_breaker(text)
    components_mapping = ranker1.map_components_to_text(components)

    result=[]
    components_from_text=[]

    for text, component in components_mapping:
        if component is not None:
            components_from_text.append(component)

    from translator.executables.nlp import grammar
    grammar.step_counter=step_number
    grammar.unrecognised_enabled=False
    components_from_text = grammar.go_through(components_from_text)
    grammar.unite_csteps(components_from_text)

    steps_list=grammar.get_new_list_with_ksteps(components_from_text)

    encode2csv.getCSVFromSteps(steps_list)

    return encode2json.EncodeStepsArrayToJSON(components_from_text)

    # for component in components_from_text:
    #     if component is not None:
    #         result.append(str(component))
    #
    # return result
