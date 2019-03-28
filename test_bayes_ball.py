from bayes_ball import *
import unittest
import shutil
import os

class TestBayesBall(unittest.TestCase):
    def setUp(self):
        shutil.copy("graph.txt", "temp_graph.txt")
        shutil.copy("queries.txt", "temp_queries.txt")


    def tearDown(self):
        shutil.copy("temp_graph.txt", "graph.txt")
        shutil.copy("temp_queries.txt", "queries.txt")

        os.remove("temp_queries.txt")
        os.remove("temp_graph.txt")

    def test_is_independent(self):

        graph_files = ["graph1.txt", "graph2.txt", "graph3.txt"]
        query_files = ["queries1.txt", "queries2.txt", "queries3.txt"]
        answer_files = ["answers1.txt", "answers2.txt", "answers3.txt"]

        for i, graph_file in enumerate(graph_files):
            print()
            print(graph_file)
            shutil.copy(graph_file, "graph.txt")
            shutil.copy(query_files[i], "queries.txt")

            answer_file = answer_files[i]
            graph = create_graph()
            Qs = read_queries()
            answers = get_answers(answer_file)

            j = 0
            for X, Y, Z in Qs:
                print("Query " + str(i+1) + "." + str(j+1) + ": Is " + str(X) + " independent of " + str(Y) + " given " + str(Z) + "?")
                actual_answer = is_independent(graph, X, Y, Z)
                expected_answer = answers[j]
                print(actual_answer, expected_answer)
                if(actual_answer != expected_answer):
                    print("!!!!!!!!!!!!!!")
                j += 1

def get_answers(file):
    answers = []
    with open(file, 'r') as a_file:
        for line in a_file:
            if line.__contains__("Yes"):
                answers.append(True)
            elif line.__contains__("No"):
                answers.append(False)
    return answers

if __name__== "__main__":
    unittest.main()