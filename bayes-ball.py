'''
Description: CS5340 - The Bayes-Ball algorithm
Name: Pawel Kostkowski, Nirav Gandhi
Matric No.: A0196329R, A********
'''


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
    return parents

def mark_v_struct(graph, Z):
    """Helper function that traverse the graph
    from leaves to the roots, marking all nodes
    that are in Z or have descendants in Z.

    Args:
        graph (dict): the Bayesian network
        Z (list): list of nodes in set Z

    Returns:
        A (list): list of nodes that are in Z of have descendants in Z
    """
    L = Z
    A = []
    while len(L) != 0:
        C = L.pop()
        if C not in A:
            for parent in get_parents(graph, C):
                L = L.push(parent)
        A = A.push(C)
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

    Returns:

    """
    q = queue.Queue()
    visited = {}

    for x in X:
        q.put(x) #this might be optimized as there might be node that will be visited multiple times
    while not q.empty():
        node = q.get()
        visited[node] = True
        if node in Y:
            return False
        if node not in Z:
            for descendant in graph[node]:
                if not visited[descendant]:
                    q.put(descendant)
    else:
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
    out = mark_v_struct(graph, Z)
    for x in X:
        if x in out:
            return False
    for y in Y:
        if y in out:
            return False
    #Phase 2
    ans = traverse_trails(graph, X, Y, out)

    return ans


if __name__ == '__main__':
    graph = create_graph()
    Qs = read_queries()
    for X, Y, Z in Qs:
        output = 1 if is_independent(graph, X, Y, Z) else 0
        print(output)
