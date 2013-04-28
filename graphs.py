""" A library including some basic graph-related algorithms.
Requires networkx or a networkx-compatible graph class to work properly."""
from __future__ import division, print_function
import collections

def maximum_matching(graph, p1):
    """ Finds a maximum matching within a bipartite graph; the required
    inputs are the graph (as a networkx.Graph) and the sequence of
    nodes corresponding to one part of the bipartite graph.
    
    The approach used is to construct a maximal matching, and then augment
    it by finding augmenting paths with a breadth-first search.
    
    Matches are stored as a dictionary that stores the matching partner for
    each node; this is what is returned. Consequently, the number of edges
    in the matching is precisely len(matches) // 2.
    """
    # First construct a maximal matching.
    matches = {}
    for n in p1: # Match every node that we can.
        for n2 in graph.neighbors(n):
            if n2 not in matches:
                matches[n] = n2
                matches[n2] = n
                break
    # Now upgrade it via augmenting paths.
    bads = set()
    for n in p1:
        if n in bads or n in matches:
            continue
        path, visited = find_augmenting_path(graph, n, matches, bads)
        if path is None: # No path found - all visited nodes must be dead ends.
            bads.update(visited) 
            continue
        for n1, n2 in path: # The path was found
            matches[n1] = n2
            matches[n2] = n1
    return matches

def find_augmenting_path(graph, node, matches, bads):
    """ Finds augmenting paths for a matching of a bipartite graph.

    The path must start from the given node; breadth-first search is used,
    ensuring that nodes are not revisited.
    
    The input matches must be a dictionary which only contains partnered
    nodes, and stores the partner for every node that has one.

    The "bads" parameter is a set of all nodes that are marked as "bad"
    and cannot be included - usually this would be because they failed
    in previous searches and hence cannot be part of an augmenting path.

    The first output is the path found, as a sequence consisting of only
    the edges that should be in the matching, or None if no path was found.
    The second output is the set of nodes that were visited; if no 
    path was found, these nodes cannot be in any future augmenting paths.
    """
    visited = set([node]) # The nodes we've visited.
    current_level = [node] # The current level of the search.
    previous = {node:None} # Our search history tree.
    while current_level:
        next_level = []
        for n in current_level:
            for n2 in graph.neighbors(n):
                if n2 in visited: 
                    continue # Nodes only need to be visited once.
                visited.add(n2)
                n3 = matches.get(n2)
                if n2 in bads or n3 in bads:
                    continue # Ignore nodes that have been marked as "bad".
                previous[n2] = n
                if n3 is None: # Return the solution as a list of edge pairs.
                    path = [(n2, n)]
                    node = n
                    while previous[node] is not None:
                        n1 = node = previous[node]
                        n2 = node = previous[node]
                        path.append((n1, n2))
                    return path, visited
                visited.add(n3)
                previous[n3] = n2
                next_level.append(n3)
        current_level = next_level
    return None, visited
