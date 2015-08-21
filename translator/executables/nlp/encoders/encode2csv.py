import csv
from io import StringIO
from operator import attrgetter

__author__ = 'NBUCHINA'


def write_csv_from_states(states, csv_file):
    state_writer = csv.writer(csv_file, delimiter=',',
                              quotechar='"', quoting=csv.QUOTE_MINIMAL)
    existing_ids = []
    for state in states:
        existing_ids.append(state.ID)

    for state in states:
        if state.next_ID not in existing_ids:
            state.next_ID = -1

    for state in states:
        step_commands = "|".join([str(x) for x in state.commands])
        state_id = int(str(state.ID).replace(".", ""))
        next_state_id = int(str(state.next_ID).replace(".", ""))
        if next_state_id < 0:
            next_state_id = ""

        state_writer.writerow(
            [state.tivipe_component_name, '1', state.description, state_id,
             step_commands.replace("\n", "").replace("\r", ""),
             next_state_id])


def write_first_csv_line(first_set_of_states, csv_file):
    state_writer = csv.writer(csv_file, delimiter=',',
                              quotechar='"', quoting=csv.QUOTE_MINIMAL)
    first_step = min(first_set_of_states, key=attrgetter('ID'))

    first_id = str(first_step.ID).replace(".", "")

    state_writer.writerow(
        ["CommandStateSelectByKey", '1', "Press S to start the scenario", 10, "[][s][%s]" % first_id])


def init_csv():
    csv_file = StringIO()
    state_writer = csv.writer(csv_file, delimiter=',',
                              quotechar='"', quoting=csv.QUOTE_MINIMAL)
    state_writer.writerow(['Component name', '--', 'Description', 'State ID', 'Robot command', 'Next state ID'])

    return csv_file