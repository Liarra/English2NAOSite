import csv
from io import StringIO

__author__ = 'NBUCHINA'


def writeCSVFromSteps(states, csvfile):
    state_writer = csv.writer(csvfile, delimiter=',',
                             quotechar='"', quoting=csv.QUOTE_MINIMAL)

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


def initCSV():
    csv_file = StringIO()
    state_writer = csv.writer(csv_file, delimiter=',',
                             quotechar='"', quoting=csv.QUOTE_MINIMAL)
    state_writer.writerow(['Component name', '--', 'Description', 'State ID', 'Robot command', 'Next state ID'])
    state_writer.writerow(
        ["CommandStateSelectByKey", '1', "Press S to start the scenario", 10, "[][s][100]"])

    return csv_file