from collections import defaultdict


def topological_sort(graph):
    """Based on the code from http://code.activestate.com/recipes/578272-topological-sort/
"""
    from functools import reduce

    data = defaultdict(set)
    for start_edge in graph.keys():
        for end_edge in graph[start_edge].keys():
            data[end_edge].add(start_edge)

    # Ignore self dependencies.
    for k, v in data.items():
        v.discard(k)

    # Find all items that don't depend on anything.
    extra_items_in_deps = reduce(set.union, data.values()) - set(data.keys())

    # Add empty dependences where needed
    data.update({item: set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item, dep in data.items() if not dep)
        if not ordered:
            break
        yield ordered
        data = {item: (dep - ordered)
                for item, dep in data.items()
                if item not in ordered}
    assert not data, "Cyclic dependencies exist among these items:\n%s" % '\n'.join(repr(x) for x in data.items())


def longest_path_DAG(graph, start_node, end_node):
    """http://www.geeksforgeeks.org/find-longest-path-directed-acyclic-graph/"""
    # TOPOLOGICALLY SORT THE VERTICES
    order = []
    for part in topological_sort(graph):
        order.extend(list(part))
    # order.reverse()

    # INITIALIZE DISTANCE MATRIX
    lowest_dist = -99999999999999999
    dist = dict((x, lowest_dist) for x in graph.keys())
    dist[start_node] = 0

    # MAIN PART
    comes_from = dict()
    for node in order:  # u

        for nbr in graph[node].keys():
            nbr_dist = graph[node][nbr]
            # v
            if dist[nbr] < dist[node] + nbr_dist:
                dist[nbr] = dist[node] + nbr_dist
                comes_from[nbr] = node

    # BACKTRACKING FOR MAXPATH
    max_path = [end_node]
    while max_path[-1] != start_node:
        max_path.append(comes_from[max_path[-1]])
    max_path.reverse()

    return dist[end_node], max_path


def exhaustive(graph, start_node, end_node):
    max_dist = -1
    max_path = []
    stack = [([start_node], 0)]
    while stack:
        cpath, cdist = stack.pop()
        cnode = cpath[-1]
        if cnode == end_node:
            if cdist > max_dist:
                max_dist = cdist
                max_path = cpath
            continue

        for end_edge in graph[cnode].keys():
            stack.append((cpath + [end_edge], cdist + graph[cnode][end_edge]))

    return max_dist, max_path


if __name__ == "__main__":
    graph = {0: [(1, 935.5), (2, 147297.5)], 1: [(3, 1e-10), (4, 945.8)],
             2: [(3, 1e-10), (4, 945.8)], 3: [(5, 3656)], 4: [(6, 7669.5), (7, 18500.5)],
             5: [(6, 7669.5), (7, 18500.5)], 6: [(8, 100)], 7: [(8, 100)], 8: []}
    start_node, end_node = 0, 8

    max_dist, max_path = exhaustive(graph, start_node, end_node)
    print("max_dist is %d, max_path is %s" % (max_dist, max_path))

    max_dist, max_path = longest_path_DAG(graph, start_node, end_node)
    print("max_dist is %d, max_path is %s" % (max_dist, max_path))

    # Example at http://www.geeksforgeeks.org/find-longest-path-directed-acyclic-graph/
    graph = {0: [(1, 5), (2, 3)], 1: [(3, 6), (2, 2)],
             2: [(4, 4), (5, 2), (3, 7)], 3: [(5, 1), (4, -1)],
             4: [(5, -2)], 5: []}
    start_node, end_node = 0, 5

    max_dist, max_path = exhaustive(graph, start_node, end_node)
    print("max_dist is %d, max_path is %s" % (max_dist, max_path))

    max_dist, max_path = longest_path_DAG(graph, start_node, end_node)
    print("max_dist is %d, max_path is %s" % (max_dist, max_path))
