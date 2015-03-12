from translator.executables.nlp.component import *
from translator.executables.nlp.execution import *
from translator.executables.nlp.ranker import text_breaker
from translator.executables.nlp.robot_commands import *

__author__ = 'NBUCHINA'



def translate(text):
    components = [say_command, wait_command,
                  move_command,
                  button_press, sequence, parallel]

    ranker1 = text_breaker(text)
    components_mapping = ranker1.map_components_to_text(components)

    result=[]
    for text, component in components_mapping:
        if component is not None:
            result.append(str(component))

    return result
