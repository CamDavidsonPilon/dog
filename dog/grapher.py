import sys
from operator import add
from functools import reduce
from .errors import error, errors_reported
from .checker import CheckProgramVisitor
from .ast import *
from collections import defaultdict
from numpy import random as random
import numpy as np
import pandas as pd
from statsmodels import api as sm


N = 1000
noise = lambda : random.randn(N)

UNDEFINED = 'undefined'
DEFINED = 'defined'


class Grapher():

    def __init__(self, checker):
        self.graph = checker.graph

    def plot(self):

        import networkx as nx
        import numpy as np
        import matplotlib.pyplot as plt
        import pylab
        from networkx.drawing.nx_agraph import graphviz_layout

        edge_labels= {(u,v,): d['weight']
                     for u,v,d in self.graph.edges(data=True)
                     if d['weight'] is not None
                     }
        node_labels = {node:node for node in self.graph.nodes()};

        pos = graphviz_layout(self.graph, prog='dot', args='')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        nx.draw_networkx_labels(self.graph, pos, labels=node_labels)
        nx.draw_networkx(self.graph, pos, node_color="#d3d3d3", node_size=1200, edge_color='black', linewidths=1.0)
        plt.axis('off')
        pylab.show()


def graph_dag(program):

    from .parser import parse

    ast = parse(program)
    checker = CheckProgramVisitor()
    checker.visit(ast)

    if errors_reported() > 0:
        sys.exit()

    graph = Grapher(checker)

    return graph.plot()


def main():
    '''
    Main program. Used for testing
    '''
    import sys

    if len(sys.argv) < 2:
        sys.stderr.write('Usage: python3 -m dog.grapher filename\n')
        raise SystemExit(1)

    graph_dag(open(sys.argv[1]).read())

if __name__ == '__main__':
    main()
