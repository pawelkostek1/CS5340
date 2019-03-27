'''
Description: CS5340 - The Bayes-Ball algorithm
Name: Pawel Kostkowski, Nirav Gandhi
Matric No.: A0196329R, A0088471W
'''

import queue
import copy

def create_graph():
    """Reads graph.txt and returns a dictionary
    with nodes as keys and the value is a list of
    nodes that the given node has a directed edge to.

    Returns:
        dict: the graph as a dictionary
    """
    with open('graph.txt', 'r') as g_file:
        K = int(g_file.readline())
        graph = {i: [] for i in range(1, K + 1)}
        for line in g_file:
            i, j = map(int, line.split())
            graph[i].append(j)
    return graph


def read_queries():
    """Reads queries.txt and returns a list of X, Y, Z
    triplets.

    Returns:
        list: the list of queries
    """
    with open('queries.txt', 'r') as q_file:
        queries = []
        for line in q_file:
            X, Y, Z = [], [], []
            x, y, z = line.split()
            X.extend(map(int, filter(bool, x[1:-1].split(','))))
            Y.extend(map(int, filter(bool, y[1:-1].split(','))))
            Z.extend(map(int, filter(bool, z[1:-1].split(','))))
            queries.append([X, Y, Z])
    return queries

def get_parents(graph, node):
    """Helper function that return a list
    of parents for a given node in a graph

    Args:
        graph (dict): the Bayesian network
        node (int): a node of the graph

    Returns:
        parents(list): the list of parents for a given node
    """
    parents = []

    for parent in graph:
        if node in graph[parent]:
            parents.append(parent)
    return parents

def  mark_v_struct(graph, Z):
    """Helper function that traverse the graph
    from leaves to the roots, marking all nodes
    that are in Z or have descendants in Z.

    Args:
        graph (dict): the Bayesian network
        Z (list): list of nodes in set Z

    Returns:
        A (list): list of nodes that are in Z or have descendants in Z
    """
    A = []
    for z in Z:
        l = [z]
        a = []
        while len(l):
            C = l.pop()
            if C not in A:
                for parent in get_parents(graph, C):
                    if parent not in Z:
                        l.append(parent)
                a.append(C)
        A.append(a)
    return A

def traverse_trails(graph, X, Y, Z):
    """Helper function that traverse all the trails
    in the graph looking for a blocked node.
    Implemented as BFS algorithm

    Args:
        graph (dict): the Bayesian network
        X (list): list of nodes in set X
        Y (list): list of nodes in set Y
        Z (list): list of nodes in set Z
        out (list): list of nodes that are in Z or have descendants in Z

    Returns:
        ans (bool): boolean answer corresponding to either finding blockage? or not

    """

    q = queue.Queue()
    visited = {}
    markedOnTop = {}
    markedOnBotton = {}
    from_child = 0
    from_parent = 1

    for node in graph:
        visited[node] = False
        markedOnBotton[node] = False
        markedOnTop[node] = False

    for x in X:
        q.put((x,from_child))

    while not q.empty():
        item = q.get()

        node = item[0]
        from_const = item[1]
        visited[node] = True

        #if visit is from child
        if from_const == from_child:
            #1. Confirm that j does not belong in K
            if not markedOnTop[node]: #if the top of j is not marked
                markedOnTop[node] = True
                for parent in get_parents(graph, node):
                    q.put((parent, from_child))
            if not markedOnBotton[node]: #if the bottom of j is not marked
                markedOnBotton[node] = False
                for child in graph[node]:
                    q.put((child, from_parent))
        else:#if visit is from parent
            if node in Z and not markedOnTop[node]:
                markedOnTop[node] = True
                for parent in get_parents(graph, node):
                    q.put((parent, from_child))
            elif node not in Z and not markedOnBotton[node]:
                markedOnBotton[node] = True
                for child in graph[node]:
                    q.put((child, from_parent))

    for y in Y:
        if visited[y]:
           return False

    return True

def is_independent(graph, X, Y, Z):
    """Checks if X is conditionally independent
    of Y given Z.

    Args:
        graph (dict): the Bayesian network
        X (list): list of nodes in set X
        Y (list): list of nodes in set Y
        Z (list): list of nodes in set Z

    Returns:
        bool: True if X is conditionally independent
    of Y given Z, False otherwise.
    """
    #Phase 1

    # out = mark_v_struct(graph, Z) # Should the v structure be done separately for every z in Z
    # #Need to check whether this is correct
    # for v_struct in out:
    #     for y in Y:
    #         for x in X:
    #             if (x in v_struct) and (y in v_struct):
    #                 return False
    #Phase 2
    #print(X)
    #print(Y)
    #print(Z)
    ans = traverse_trails(graph, X, Y, Z)

    return ans


if __name__ == '__main__':
    graph = create_graph()
    print("Graph:")
    print(graph)

    Qs = read_queries()
    i = 1
    for X, Y, Z in Qs:
        print("Query " + str(i) + ": Is " + str(X) + " independent of " + str(Y) + " given " + str(Z) + "?")
        output = 1 if is_independent(graph, X, Y, Z) else 0
        if output:
            print("Yes")
        else:
            print("No")
        i += 1
