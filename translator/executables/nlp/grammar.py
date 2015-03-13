from translator.executables.nlp.components.component import *
from translator.executables.nlp.step import step

__author__ = 'NBUCHINA'

gone_through = False
step_counter = 1
step_modifier = 1


def go_through(components):
    global step_counter
    global step_modifier

    new_list = []
    gone_through = True

    i = 0
    while i < len(components):

        if i < len(components) - 1:

            if isinstance(components[i], unrecognised_component) & isinstance(components[i + 1],
                                                                              unrecognised_component):
                unrec1 = components[i]
                unrec2 = components[i + 1]
                new_list.append(
                    unrecognised_component(unrec1.description + " " + unrec2.description, unrec1.text_index_start))

                gone_through = False
                i += 1



            # elif isinstance(components[i], condition) & isinstance(components[i + 1], component):
            #     cond = components[i]
            #     action = components[i + 1]
            #
            #     new_step = step()
            #     new_step.text_index_start=cond.text_index_start
            #     new_step.component_name = cond.component_name
            #     new_step.description = cond.description + " " + action.description
            #     new_step.state_ID = step_counter
            #     new_step.commands.append(action)
            #     new_step.condition.append(cond)
            #
            #     step_counter += step_modifier


            else:
                new_list.append(components[i])



        else:
            new_list.append(components[i])
        i += 1

    if gone_through:
        return new_list
    else:
        return go_through(new_list)