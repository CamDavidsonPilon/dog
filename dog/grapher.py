import sys
from operator import add
from functools import reduce
from .errors import error, errors_reported
from .checker import check_program
from .ast import *
from collections import defaultdict
from numpy import random as random
import numpy as np
import pandas as pd
from statsmodels import api as sm
import argparse


class Grapher():

    def __init__(self, checker):
        self.graph = checker.graph

    def plot(self, output=None, show=True):

        def mark_unobserved(label, data):
            if not data['observed']:
                return "(" + label + ")"
            return label

        def resize_label_size(label):
            if len(label) < 16:
                return label
            else:
                words = label.split("_")
                word_lengths = [len(w) for w in words]
                # try to balance 2 lines
                arg_smallest_delta = np.argmin([
                    abs(sum(word_lengths[i:]) - sum(word_lengths[:i])) for i in range(1, len(words))
                ]) + 1 # plus 1 because we started at one
                return "_".join(words[:arg_smallest_delta]) + "_\n" + "_".join(words[arg_smallest_delta:])


        import networkx as nx
        import numpy as np
        import matplotlib.pyplot as plt
        import pylab
        from networkx.drawing.nx_agraph import graphviz_layout

        fig = plt.figure(figsize=(8, 7))
        ax = plt.subplot(1,1,1)

        edge_labels= {(u,v,): d['weight']
                     for u,v,d in self.graph.edges(data=True)
                     if d['weight'] is not None
                     }
        node_labels = {node: mark_unobserved(resize_label_size(node), data) for node, data in self.graph.nodes(data=True)}

        node_colors = ["#d3d3d3" if d.get('observed', False) else "#9ebbc6" for node, d in self.graph.nodes(data=True)]


        pos = graphviz_layout(self.graph, prog='neato')

        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        nx.draw_networkx(self.graph, pos, node_color=node_colors, node_size=2000,
                         edge_color='black', linewidths=1.0, width=1.5, labels=node_labels,
                         arrowsize=15, ax=ax, font_size=12)
        plt.axis('off')

        if output:
            plt.savefig(output, dpi=275, bbox_inches='tight')

        if show:
            pylab.show()


def graph_dag(program, output, show):

    from .parser import parse

    ast = parse(program)
    checker = check_program(ast)

    if errors_reported() > 0:
        sys.exit()

    graph = Grapher(checker)

    return graph.plot(output, show)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the .dg filename to graph")
    parser.add_argument("-o", "--output", help="name of the file to save the image to")
    parser.add_argument('--no-show', help='suppress showing the graph in the UI', action="store_false")
    args = parser.parse_args()

    graph_dag(open(args.filename).read(), args.output, args.no_show)

if __name__ == '__main__':
    main()
