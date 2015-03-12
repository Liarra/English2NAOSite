class component(object):
    tags = []
    regexp = ""

    def __init__(self, name):
        self.name = name;

    def __repr__(self):
        return self.name

    def parse_from_string(self, string):
        pass


class button_press(component):
    tags = [ "press", "button"]
    regexp = r"(press|type) ['\"]?(?P<button>.)['\"]?[ ,.]?"

    button = ''

    def __init__(self, string):
        import re

        p = re.compile(self.regexp, re.IGNORECASE)
        string = string.strip()
        string = string.lower()

        m = p.search(string)
        if (m == None):
            return
        button = m.group('button')

        self.button = button

    def __repr__(self):
        return "key[%s]->" % self.button


class button_input_component(component):
    pass


class unrecognised_component(component):
    unrecognised_text = ""
    tags = []
    regexp = ""

    def __init__(self, string):
        self.unrecognised_text = string

    def __repr__(self):
        return "_UNRECOGNISED_[%s]" % self.unrecognised_text