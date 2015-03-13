from translator.executables.nlp.components.component import button_press, unrecognised_component
from translator.executables.nlp.components.execution import sequence, parallel
from translator.executables.nlp.ranker import text_breaker
from translator.executables.nlp.components.robot_commands import *


components = [say_command, wait_command, move_command, button_press, sequence, parallel]



# text="When I press 'Y', robot should say 'Yes master'"
#text="The robot says 'hi', then waits for 5 seconds."

text = '''The robot says 'hi', then waits for 5 seconds. Then it tells 'My name is NAO'.
Then it starts dancing, jumping, telling 'I am funny'. Then it stops and waits for 20 seconds. When I press y, it
bursts out laughing and waves'''

# text='''The scenario starts with the robot saying “hi <name child>” and providing a hand at the same time.
# When the child touches the hand of the robot, this is rewarded by saying “thank you” (press y) and the robot shaking
# the hand of the child (natural reward) . However, when the child does not show appropriate behavior, I want to provide
# prompts (press n), e.g. levels of help to the child.'''

#text="When the child touches the hand of the robot, this is rewarded by saying “thank you” (press y)"

#text="Then it tells 'My name is NAO'."
# text = '''Then it tells 'My name is NAO'.
# Then it starts dancing, jumping, telling 'I hate you so much you stupid humans'.'''
#text=input("Enter your requirement:\n")
ranker1 = text_breaker(text)
#ranker2 = text_breaker(text2)
#components_mapping= (ranker1.map_components_to_graph(components))
#maxdist, maxpath = longestpath.exhaustive(graph, 0, len(text))
components_mapping = ranker1.map_components_to_text(components)
print(components_mapping)
print()

components_from_text = []
for text, component in components_mapping:
    if component is not None:
        components_from_text.append(component)

from translator.executables.nlp import grammar

components_from_text = grammar.go_through(components_from_text)

i = 0
for component in components_from_text:
    print("%d. %s" % (i, component))
    i += 1

print("")

i = 0;
for component in components_from_text:
    if component.__class__ is not unrecognised_component:
        print("%d. %s" % (i, component))
        i += 1
        #print (ranker2.map_components_to_text(components))