from collections import defaultdict

def toposort(graph):
    """http://code.activestate.com/recipes/578272-topological-sort/
    
    Dependencies are expressed as a dictionary whose keys are items
and whose values are a set of dependent items. Output is a list of
sets in topological order. The first set consists of items with no
dependences, each subsequent set consists of items that depend upon
items in the preceeding sets.

>>> print '\\n'.join(repr(sorted(x)) for x in toposort2({
...     2: set([11]),
...     9: set([11,8]),
...     10: set([11,3]),
...     11: set([7,5]),
...     8: set([7,3]),
...     }) )
[3, 5, 7]
[8, 11]
[2, 9, 10]

"""
    from functools import reduce
    data = defaultdict(set)
    # for x, y in graph.items():
    for start_edge in graph.keys():
        for end_edge in graph[start_edge].keys():
        # for z in y:
            data[end_edge].add(start_edge)

    # Ignore self dependencies.
    for k, v in data.items():
        v.discard(k)
    # Find all items that don't depend on anything.
    extra_items_in_deps = reduce(set.union, data.values()) - set(data.keys())
    # Add empty dependences where needed
    data.update({item:set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item, dep in data.items() if not dep)
        if not ordered:
            break
        yield ordered
        data = {item: (dep - ordered)
                for item, dep in data.items()
                    if item not in ordered}
    assert not data, "Cyclic dependencies exist among these items:\n%s" % '\n'.join(repr(x) for x in data.items())

def longestpathDAG(graph, startnode, endnode):
    """http://www.geeksforgeeks.org/find-longest-path-directed-acyclic-graph/"""
    ### TOPOLOGICALLY SORT THE VERTICES
    order = []
    for part in toposort(graph):
        order.extend(list(part))
    # order.reverse()

    ### INITIALIZE DISTANCE MATRIX
    LOWDIST=-99999999999999999
    dist = dict((x, LOWDIST) for x in graph.keys())
    dist[startnode] = 0

    ### MAIN PART
    comesfrom = dict()
    for node in order: # u

        for nbr in graph[node].keys():
            nbrdist=graph[node][nbr]
        # for nbr, nbrdist in graph[node]: # v
            if dist[nbr] < dist[node] + nbrdist:
                dist[nbr] = dist[node] + nbrdist
                comesfrom[nbr] = node

    ### BACKTRACKING FOR MAXPATH
    maxpath = [endnode]
    while maxpath[-1] != startnode:
        maxpath.append(comesfrom[maxpath[-1]])
    maxpath.reverse()

    return dist[endnode], maxpath

def exhaustive(graph, startnode, endnode):
    maxdist = -1
    stack = [([startnode], 0)]
    while stack:
        cpath, cdist = stack.pop()
        cnode = cpath[-1]
        if cnode == endnode:
            if cdist > maxdist:
                maxdist = cdist
                maxpath = cpath
            continue
            
        for end_edge in graph[cnode].keys():
            stack.append( (cpath+[end_edge], cdist+graph[cnode][end_edge]) )

        '''for nbr, nbrdist in graph[cnode]:
            stack.append( (cpath+[nbr], nbrdist+cdist) )'''

    return maxdist, maxpath

if __name__ == "__main__":

    graph = {0:[(1, 935.5), (2, 147297.5)], 1:[(3, 1e-10), (4, 945.8)],
             2:[(3, 1e-10),(4, 945.8)], 3:[(5, 3656)], 4:[(6, 7669.5), (7, 18500.5)],
             5:[(6, 7669.5), (7, 18500.5)], 6:[(8, 100)], 7:[(8, 100)], 8:[]}
    startnode, endnode = 0, 8

    maxdist, maxpath = exhaustive(graph, startnode, endnode)
    print("Maxdist is %d, maxpath is %s" % (maxdist, maxpath))

    maxdist, maxpath = longestpathDAG(graph, startnode, endnode)
    print("Maxdist is %d, maxpath is %s" % (maxdist, maxpath))

    # Example at http://www.geeksforgeeks.org/find-longest-path-directed-acyclic-graph/
    graph = {0:[(1, 5), (2, 3)], 1:[(3, 6), (2, 2)],
             2:[(4, 4), (5, 2), (3, 7)], 3:[(5, 1), (4, -1)],
             4:[(5, -2)], 5:[]}
    startnode, endnode = 0, 5

    maxdist, maxpath = exhaustive(graph, startnode, endnode)
    print("Maxdist is %d, maxpath is %s" % (maxdist, maxpath))

    maxdist, maxpath = longestpathDAG(graph, startnode, endnode)
    print("Maxdist is %d, maxpath is %s" % (maxdist, maxpath))
