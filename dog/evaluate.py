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

    def regression(self, variables):
        df = pd.DataFrame({
            v: self.global_variables[v] for v in variables
        })
        df = sm.tools.add_constant(df)
        return sm.OLS(self.global_variables['O'], df).fit().summary()


def evaluate_program(program, proposed_formula):

    from .parser import parse

    ast = parse(program)
    checker = check_program(ast)
    eval = Evaluator(checker)

    formula_ast = parse(proposed_formula)
    formula_checker = check_program(formula_ast)
    formula_vars = formula_checker.graph.predecessors('O')

    return eval.regression(formula_vars)


def main():
    '''
    Main program. Used for testing
    '''
    import sys

    if len(sys.argv) < 2:
        sys.stderr.write('Usage: python3 -m dog.evaluate filename formula\n')
        raise SystemExit(1)

    print(evaluate_program(open(sys.argv[1]).read(), sys.argv[2]))

if __name__ == '__main__':
    main()
