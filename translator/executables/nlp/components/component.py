class component(object):
    tags = []
    regexp = ""

    component_name = ""
    description = ""
    text_index_start = 0
    command = ""

    def __init__(self, string, index_in_text=0):
        string = string.strip()
        string = string.lower()
        self.description = string
        self.text_index_start=index_in_text

    def __repr__(self):
        return self.command

    def parse_from_string(self, string):
        pass


class condition(component):
    pass

class button_press(condition):
    tags = ["press", "button"]
    regexp = r"(press|type) ['\"]?(?P<button>.)['\"]?\W?$"

    button = ''

    def __init__(self, string, index_in_text=0):
        super().__init__(string,index_in_text)
        self.component_name = "CommandStateSelectByKey"

        import re

        p = re.compile(self.regexp, re.IGNORECASE)
        string = string.strip()
        string = string.lower()
        m = p.search(string)
        if (m is None ):
            return
        button = m.group('button')
        self.button = button
        self.command = "key[%s]->" % self.button


class unrecognised_component(component):
    unrecognised_text = ""
    tags = []
    regexp = ""

    def __init__(self, string, index_in_text=0):
        super().__init__(string,index_in_text)
        self.unrecognised_text = string
        self.command = "_UNRECOGNISED_[%s]" % self.unrecognised_text