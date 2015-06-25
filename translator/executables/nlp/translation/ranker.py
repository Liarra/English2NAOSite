from translator.executables.nlp.translation import longestpath
from translator.executables.nlp.components.component import unrecognised_component


class text_breaker(object):
    def __init__(self, text):
        self.text = text.replace("\n", " ")
        self.graph = self._build_graph_for_text_(self.text)
        self.components_mapping = {}
        self.ranker = ranker()

    def map_components_to_text(self, components):
        components_mapping = (self.map_components_to_graph(components))
        maxdist, maxpath = longestpath.longestpathDAG(self.graph, 0, len(self.text))

        text_to_components = []
        for i in range(0, len(maxpath) - 1):
            text_piece = self.text[maxpath[i]: maxpath[i + 1]]
            text_piece = text_piece.strip()
            component = components_mapping[maxpath[i]][maxpath[i + 1]]

            if component is not None:
                component_object = component.from_string(text_piece)
            else:
                component_object = unrecognised_component.from_string(text_piece)

            text_to_components.append((text_piece, component_object))

        return text_to_components


    def map_components_to_graph(self, components):
        edges_to_components = {}
        for edge_start in self.graph.keys():
            edges_to_components[edge_start] = {}

            for edge_end in self.graph[edge_start].keys():
                edges_to_components[edge_start][edge_end] = None
                old_rank = self.graph[edge_start][edge_end]

                for component in components:
                    component_rank = self.ranker.rank_component(self.text[edge_start: edge_end], component)
                    new_rank = component_rank + self.ranker.rank_chunk(self.text[edge_start: edge_end])
                    # print ("%d-%d:%d"%(edge_start, edge_end, new_rank))
                    if new_rank > old_rank:
                        self.graph[edge_start][edge_end] = new_rank
                        old_rank = new_rank
                        if component_rank > 0:
                            #print("assigning %s to '%s' with rank %d" % (component, self.text[edge_start: edge_end], new_rank))
                            edges_to_components[edge_start][edge_end] = component

        self.components_mapping = edges_to_components
        # print (self.graph)
        return edges_to_components

    def _build_graph_for_text_(self, text):
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
                connections[edges[j]] = 0
            graph[edges[i]] = connections

        return graph


class ranker(object):
    def rank_chunk(self, text):
        rank = 0
        rank += self.rankLength(text)
        rank += self.rankPunctuation(text)

        return rank

    def rank_component(self, text, component):
        rank = 0
        rank += self.rankTags(text, component)
        rank += self.rankRegexp(text, component)
        # print (rank)
        return rank

    def rankTags(self, text, component):
        # edge_text=self.text[edge_start:edge_end]
        text = text.lower()
        sum = 0
        for tag in component.tags:
            if tag in text:
                sum += 5
        rank = sum
        return rank

    def rankRegexp(self, text, component):
        import re

        p = re.compile(component.regexp, re.IGNORECASE)
        text = text.strip()
        if p.match(text):
            # print (p.match(text))
            return 15
        return 0

    def rankLength(self, text):
        shortest = 3
        longest = 500
        if len(text) > longest or len(text) < shortest:
            return -5
        return 0

    def rankPunctuation(self, text):
        signs = ['.', ',']
        text = text.rstrip()
        if len(text) < 1: return 0
        if text[len(text) - 1] in signs:
            return 5
        return 0