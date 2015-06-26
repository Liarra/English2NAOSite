from collections import OrderedDict

__author__ = 'nina'


class Grammar:
    def __init__(self):
        self.rules = OrderedDict()
        self.word_names = OrderedDict()

    def appendRule(self, input, transformation=None):
        names_array = []
        things_array = []
        for name, thing in input:
            names_array.append(name)
            things_array.append(thing)

        self.rules[tuple(things_array)] = transformation
        self.word_names[tuple(things_array)] = tuple(names_array)


    def process(self, objects_stream):
        return []