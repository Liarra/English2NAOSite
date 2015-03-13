from translator.executables.nlp.components.component import component

__author__ = 'NBUCHINA'


class sequence(component):
    tags = ["after", "then", "next"]
    regexp = r"(then|next)$"

    def __init__(self, string, index_in_text=0):
        super().__init__(string,index_in_text)
        self.command = " & "


class parallel(component):
    tags = ["same time"]
    regexp = r"^\ ?(and|while)$"

    def __init__(self, string, index_in_text=0):
        super().__init__(string,index_in_text)
        self.command = " | "