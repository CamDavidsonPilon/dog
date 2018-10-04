import sys
from warnings import warn
from operator import add
from functools import reduce
from .errors import error, errors_reported
from .checker import check_program, UNDEFINED, DEFINED
from .utils import satisfies_backdoor_criteria
from .ast import *
from collections import defaultdict
import numpy as np
import pandas as pd
from statsmodels import api as sm
from numpy import random as random
import argparse



class Evaluator():

    def __init__(self, checker, seed=41, sample_size=20000):
        np.random.seed(seed)
        self.sample_size = sample_size
        self.global_variables = {
            name: self.noise() if defined == UNDEFINED else None
            for (name, defined) in
            checker.global_variables.items()
        }
        self.graph = checker.graph
        for node in self.graph:
            self.evaluate_graph(node)

    def noise(self):
        v = random.randn(self.sample_size)
        return v


    def evaluate_graph(self, variable):
        if self.global_variables[variable] is not None:
            return self.global_variables[variable]

        results = np.zeros(self.sample_size)
        for parent in sorted(self.graph.predecessors(variable)):
            if self.global_variables[parent] is None:
                self.evaluate_graph(parent)

            weight = self.graph.get_edge_data(parent, variable)['weight']
            if weight is None:
                weight = random.randint(-10, 10)
            results = results + weight * self.global_variables[parent]

        results += self.noise()
        self.global_variables[variable] = results
        return self.global_variables[variable]

    def regression(self, variables):
        variables = set(variables)
        controlling_variables = variables.difference(['E', 'O'])

        if not satisfies_backdoor_criteria(self.graph, 'E', 'O', controlling_variables):
            warn("Controlling variables, %s, does not satifies back-door criteria." % list(controlling_variables))

        df = pd.DataFrame({
            v: self.global_variables[v] for v in variables
        })
        df = df.sort_index(axis=1)
        df = sm.tools.add_constant(df)
        return sm.OLS(self.global_variables['O'], df).fit().summary()


def evaluate_program(program, proposed_formula, seed, sample_size):

    from .parser import parse

    ast = parse(program)
    checker = check_program(ast, check_exposure=True, check_outcome=True)

    eval = Evaluator(checker, seed=seed, sample_size=sample_size)
    formula_ast = parse(proposed_formula)
    formula_checker = check_program(formula_ast, check_exposure=True, check_outcome=True) # should check for 'E'
    formula_vars = formula_checker.graph.predecessors('O')
    return eval.regression(formula_vars)


def main():
    '''
    Main program. Used for testing
    '''
    import sys


    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the .dg filename to graph")
    parser.add_argument("formula", help="the formula to run")
    parser.add_argument("-s", "--seed", help="seed", type=int)
    parser.add_argument("-z", "--sample-size", help="sample size of data to generate", type=int)
    args = parser.parse_args()

    print(evaluate_program(open(args.filename).read(), args.formula, args.seed, args.sample_size))

if __name__ == '__main__':
    main()
