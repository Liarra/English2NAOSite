__author__ = 'NBUCHINA'


class SubStep(object):
    component_name = ""
    commands = []

    description = ""
    text_index_start = 0

    ID = -1
    next_ID = -1

    def __init__(self):
        self.component_name = ""
        self.commands = []

        self.description = ""
        self.text_index_start = 0

        self.ID = -1
        self.next_ID = -1


class ConditionSubStep(SubStep):
    def __init__(self):
        super().__init__()
        self.condition = []


class SelectByKeyState(SubStep):
    keys = []
    states = []
    component_name = "CommandStateSelectByKey"

    def __init__(self):
        self.component_name = "CommandStateSelectByKey"
        self.keys = []
        self.states = []

    def add_cstep(self, new_cstep):
        key = new_cstep.condition[0].button
        state = new_cstep.next_ID

        self.keys.append(key)
        self.states.append(int(float(state) * 100))
        self.reconstruct_description()

    def reconstruct_description(self):
        if len(self.keys) == 1:
            self.description = "Key selection. press " + self.keys[0]
        else:
            self.description = "Key selection. press " + ','.join(self.keys[:-1]) + " or " + self.keys[-1]
        self.commands = ["[][%s][%s]" % (",".join(self.keys), ",".join([str(x) for x in self.states]))]