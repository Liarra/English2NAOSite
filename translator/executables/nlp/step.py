__author__ = 'NBUCHINA'


class step(object):
    component_name = ""
    commands = []

    description = ""
    text_index_start = 0

    state_ID = -1
    next_state_ID = -1

    def __init__(self):
        self.component_name = ""
        self.commands = []

        self.description = ""
        self.text_index_start = 0

        self.state_ID = -1
        self.next_state_ID = -1

class cstep(step):
    def __init__(self):
        super().__init__()
        self.condition = []