"""




"""

def create_graph():
    """
    Reades graph.txt and returns a dictionary
    with nodes as kwys and the value is a list of
    nodes tht the given node has a directed edge to.

    :return:
        dict: the graph as a dictionary
    """

    with open('graph.txt','r') as g_file:
        K = int(g_file.readline())
        graph = {i: [] for i in range(1, K+1)}
        for line in g_file:
            i, j = map(int, line.split())
            graph[i].append(j)
    return graph

def read_queries():
    """
    Reads queries.txt and returns a list of X, Y, Z triplets.

    :return:
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

def is_independent(graph, X, Y, Z):
    """
    Checks if X is conditionally independent of Y given Z.
     :param
        graph (dict): the Bayesian network
        X (list): list of nodes in set X
        Y (list): list of nodes in set Y
        Z (list): list of nodes in set Z
    :return:
        bool: True if X is conditionally independent of Y given Z, False otherwise
    """
    #TODO
    return True

if __name__ == '__main__':
    graph = create_graph()
    Qs = read_queries()
    for X, Y, Z in Qs:
        output = 1 if is_independent(graph, X, Y, Z) else 0
        print(output)

