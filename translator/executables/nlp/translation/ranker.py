from translator.executables.nlp.translation import longestpath
from translator.executables.nlp.components.component import UnrecognisedComponent, IgnoredComponent


class TextBreaker(object):
    def __init__(self, text):
        self.text = text.replace("\n", " ")
        self.graph = self._build_graph_for_text_(self.text)
        self.components_mapping = {}
        self.ranker = Ranker()

    def get_components(self, components):
        components_mapping = (self._map_components_to_graph_(components))
        maxdist, maxpath = longestpath.longest_path_DAG(self.graph, 0, len(self.text))

        text_to_components = []
        for i in range(0, len(maxpath) - 1):
            text_piece = self.text[maxpath[i]: maxpath[i + 1]]
            text_piece = text_piece.strip(' .,')
            if text_piece == ' ' or len(text_piece) == 0:
                continue
            component = components_mapping[maxpath[i]][maxpath[i + 1]]

            if component is not None:
                component_object = component.from_string(text_piece)
                # If failed to initialise the component
                if component_object is None:
                    component_object = UnrecognisedComponent.from_string(text_piece)
            else:
                component_object = UnrecognisedComponent.from_string(text_piece)

            text_to_components.append((text_piece, component_object))

        return text_to_components

    def _map_components_to_graph_(self, components):
        edges_to_components = {}
        for edge_start in self.graph.keys():
            edges_to_components[edge_start] = {}

            for edge_end in self.graph[edge_start].keys():
                edges_to_components[edge_start][edge_end] = None
                old_rank = self.graph[edge_start][edge_end]

                for component in components:
                    component_rank = self.ranker.rank_component(self.text[edge_start: edge_end], component)
                    new_rank = component_rank + self.ranker.rank_chunk(self.text[edge_start: edge_end])
                    if new_rank > old_rank:

                        self.graph[edge_start][edge_end] = new_rank
                        old_rank = new_rank
                        if component_rank > 0:
                            edges_to_components[edge_start][edge_end] = component

        self.components_mapping = edges_to_components
        return edges_to_components

    @staticmethod
    def _build_graph_for_text_(text):
        edges = [0]
        i = 0
        for c in text:
            if c in [' ']:
                edges.append(i)
            i += 1

        edges.append(len(text))

        graph = {}
        for i in range(0, len(edges)):
            connections = {}
            for j in range(i + 1, min(len(edges), i + 100)):
                connections[edges[j]] = 0.0000001
            graph[edges[i]] = connections

        return graph


class Ranker(object):
    price_for_tag = 5
    price_for_ignored = 0.2
    price_for_regexp = 15
    price_for_length = -2
    price_for_punctuation = 5

    def rank_chunk(self, text):
        rank = 0
        text = text.strip(',. ')
        rank += self.rank_length(text)
        rank += self.rank_punctuation(text)

        return rank

    def rank_component(self, text, component):
        rank = 0
        text = text.strip(',. ')
        rank += self.rank_tags(text, component)
        if component.regexp:
            rank += self.rank_regexp(text, component)
        return rank

    def rank_tags(self, text, component):
        import re

        price_for_tag = self.price_for_tag
        if isinstance(component, IgnoredComponent):
            price_for_tag = self.price_for_ignored

        text = text.lower()
        text_words = re.findall(r"[\w']+", text)
        tags_sum = 0
        tags_number = 0
        for tag in component.tags:
            for word in text_words:
                if tag == word:
                    tags_sum += price_for_tag
                    tags_number += 1
        rank = tags_sum + 2 * (tags_number - 1)
        return rank

    def rank_regexp(self, text, component):
        import re

        p = re.compile(component.regexp, re.IGNORECASE)
        text = text.strip()
        if p.match(text):
            match = p.match(text)
            groupdict = match.groupdict()
            if len(groupdict) > 0:
                if all(groupdict[k] is None for k in groupdict):
                    return 0

            return self.price_for_regexp
        return 0

    def rank_length(self, text):
        shortest = 2
        longest = 500
        if len(text) > longest or len(text) < shortest:
            return self.price_for_length
        return 0

    def rank_punctuation(self, text):
        signs = ['.', ',']
        text = text.rstrip()
        if len(text) < 1:
            return 0
        if text[len(text) - 1] in signs:
            return self.price_for_punctuation
        return 0