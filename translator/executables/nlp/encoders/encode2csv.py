import csv
from io import StringIO

__author__ = 'NBUCHINA'


def writeCSVFromSteps(steps, csvfile):
    step_writer = csv.writer(csvfile, delimiter=',',
                             quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for step in steps:
        step_commands = "|".join([str(x) for x in step.commands])
        ID = int(str(step.ID).replace(".", ""))
        next_ID = int(str(step.next_ID).replace(".", ""))
        if next_ID<0: next_ID=""
        # next_ID = "" if float(step.next_ID) < 0 else int(round((float(step.next_ID) * 100)))

        step_writer.writerow(
            [step.tivipe_component_name, '1', step.description, ID, step_commands.replace("\n","").replace("\r",""), next_ID])
        # print(csvfile.getvalue())


def initCSV():
    csvfile=StringIO()
    step_writer = csv.writer(csvfile, delimiter=',',
                                 quotechar='"', quoting=csv.QUOTE_MINIMAL)
    step_writer.writerow(['Component name', 'Dunno', 'Description', 'State ID', 'Command', 'Next ID'])
    step_writer.writerow(
            ["CommandStateSelectByKey", '1', "Press S to start the scenario", 10, "[][s][100]"])

    return csvfile