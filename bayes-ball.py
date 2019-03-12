'''
Description: CS5340 - The Bayes-Ball algorithm
Name: Pawel Kostkowski, Nirav Gandhi
Matric No.: A0196329R, A********
'''

import queue

def create_graph():
    """Reads graph.txt and returns a dictionary
    with nodes as keys and the value is a list of
    nodes that the given node has a directed edge to.

    Returns:
        dict: the graph as a dictionary
    """
    with open('graph2.txt', 'r') as g_file:
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
    with open('queries2.txt', 'r') as q_file:
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

def mark_v_struct(graph, Z):
    """Helper function that traverse the graph
    from leaves to the roots, marking all nodes
    that are in Z or have descendants in Z.

    Args:
        graph (dict): the Bayesian network
        Z (list): list of nodes in set Z

    Returns:
        A (list): list of nodes that are in Z or have descendants in Z
    """
    L = Z.copy()
    A = []

    while len(L):
        C = L.pop()
        if C not in A:
            for parent in get_parents(graph, C):
                L.append(parent)
            A.append(C)
    return A

def traverse_trails(graph, X, Y, Z, out):
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
    for node in graph:
        visited[node] = False

    for x in X:
        q.put(x)
    while not q.empty():
        node = q.get()
        visited[node] = True
        if node in Y:
            print("This node is in Y: " + str(node))
            return False
        if node not in Z: #is this the case?
            print(node)
            print(Z)
            for descendant in graph[node]:
                if not visited[descendant]:
                    q.put(descendant)
    #Should we do the above also for Y
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

    out = mark_v_struct(graph, Z) # Should the v structure be done separately for every z in Z
    #Need to check whether this is correct
    #for x in X:
    #    for y in Y:
    #        if (x in out) and (y in out):
    #            return False
    #Phase 2
    print(X)
    print(Y)
    print(Z)
    ans = traverse_trails(graph, X, Y, Z, out)

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
