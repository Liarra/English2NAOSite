from translator.executables.nlp.components.component import component

__author__ = 'NBUCHINA'


class sequence(component):
    tags = ["after", "then", "next"]
    regexp = r"(then|next)$"

    def __init__(self, string, index_in_text=0):
        super().__init__(string, index_in_text)
        self.command = " & "


class parallel(component):
    tags = ["same time"]
    regexp = r"^\ ?(and|while)$"

    def __init__(self, string, index_in_text=0):
        super().__init__(string, index_in_text)
        self.command = " | "


class goto(component):
    tags = []
    regexp = r"go to (step|state|point) (?P<number>\d{1,5})"
    where = -1

    def __init__(self, string, index_in_text=0):
        super().__init__(string, index_in_text)

        import re

        p = re.compile(self.regexp, re.IGNORECASE)
        string = string.strip()
        string = string.lower()

        m = p.search(string)
        if (m == None):
            return
        self.where = float(m.group('number'))

        self.command = "goto[%.2f]" % self.where
