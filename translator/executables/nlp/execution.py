from translator.executables.nlp.component import component

__author__ = 'NBUCHINA'

class sequence(component):
    tags = ["after", "then", "next"]
    regexp =r"(then|next)$"

    def __init__(self, string):
        pass

    def __repr__(self):
        return " & "

class parallel(component):
    tags = ["same time"]
    regexp = r"\W(and|while)$"

    def __init__(self, string):
        pass

    def __repr__(self):
        return " | "