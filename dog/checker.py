# checker.py
"""
this should check for no cycles

"""
import sys
from .errors import error, errors_reported
from .ast import *
from collections import defaultdict
from networkx import DiGraph
from networkx.algorithms import is_directed_acyclic_graph


UNDEFINED = 'undefined'
DEFINED = 'defined'
OUTCOME, EXPOSURE = 'O', 'E'

class CheckProgramVisitor(NodeVisitor):

    def __init__(self):
        self.global_variables = defaultdict(lambda : UNDEFINED)
        self.graph = DiGraph()
        self._outcome_found = False


    def visit_VarDeclaration(self, node):
        self.visit(node.value)
        self.global_variables[node.name] = DEFINED
        for child, weight in node.value.children:
            self.graph.add_edge(child, node.name, weight=weight)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

        if node.op == '*':
            # this is a weighted variable
            node.children = set([(node.right.name, node.left.value)])

        elif node.op == '+':
            node.children = node.left.children.union(node.right.children)

    def visit_FloatLiteral(self, node):
        node.children = set([])

    def visit_Exposure(self, node):
        node.children = set([
                    (EXPOSURE, None)
        ])

    def visit_SimpleLocation(self, node):
        self.global_variables[node.name]
        node.children = set([
            (node.name, None)
        ])

    def visit_OutcomeDeclaration(self, node):
        self._outcome_found = True
        self.visit(node.value)
        self.global_variables[OUTCOME] = DEFINED
        for child, weight in node.value.children:
            self.graph.add_edge(child, OUTCOME, weight=weight)



def check_program(ast):
    '''
    Check the supplied program (in the form of an AST)
    '''
    checker = CheckProgramVisitor()
    checker.visit(ast)
    if not is_directed_acyclic_graph(checker.graph):
        error("EOF", "Graph is not acyclic.")
    if not checker._outcome_found:
        error("EOF", "Outcome variable not defined.")

    if errors_reported() > 0:
        sys.exit()

    return checker

def main():
    '''
    Main program. Used for testing
    '''
    import sys
    from .parser import parse

    if len(sys.argv) < 2:
        sys.stderr.write('Usage: python3 -m dog.checker filename\n')
        raise SystemExit(1)

    ast = parse(open(sys.argv[1]).read())
    check_program(ast)
    for depth, node in flatten(ast):
        print('%s: %s%s' % (getattr(node, 'lineno', None), ' '*(4*depth), node))


if __name__ == '__main__':
    main()




