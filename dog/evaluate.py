# evaluate.py

"""

1. put all undefined variables into name space
2. traverse the AST, compute the dataset.

 ex:
   def visitBinOp(self, node):
      left = self.visit(node.left)
      right = self.visit(node.right)
      return left + right

    def visit_SimpleLocation(slef, node):
        return eval('%s' % node.name)

"""
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


class Evaluator():

    def __init__(self, checker):
        self.global_variables = {
            name: noise() if defined == UNDEFINED else None
            for (name, defined) in
            checker.global_variables.items()
        }
        self.graph = checker.graph
        self.evaluate_graph('O')

    def evaluate_graph(self, variable):
        results = np.zeros(N)
        for parent in self.graph.predecessors(variable):
            if self.global_variables[parent] is None:
                self.evaluate_graph(parent)

            weight = self.graph.get_edge_data(parent, variable)['weight']
            if weight is None:
                weight = random.randn()
            results = results + weight * self.global_variables[parent]

        results += noise()
        self.global_variables[variable] = results
        return self.global_variables[variable]

    def regression(self):
        df = pd.DataFrame({
            parent: self.global_variables[parent]
            for parent in self.graph.predecessors('O')
        })
        df = sm.tools.add_constant(df)
        return sm.OLS(self.global_variables['O'], df).fit().summary()


def evaluate_program(program):

    from .parser import parse

    ast = parse(program)
    checker = CheckProgramVisitor()
    checker.visit(ast)
    if errors_reported() > 0:
        sys.exit()

    eval = Evaluator(checker)

    return eval.regression()


def main():
    '''
    Main program. Used for testing
    '''
    import sys

    if len(sys.argv) < 2:
        sys.stderr.write('Usage: python3 -m dog.evaluate filename\n')
        raise SystemExit(1)

    print(evaluate_program(open(sys.argv[1]).read()))

if __name__ == '__main__':
    main()
