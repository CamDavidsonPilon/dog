from sly import Parser
from .errors import error
from .lexer import DogLexer
from .ast import *

class DogParser(Parser):
    # Same token set as defined in the lexer
    tokens = DogLexer.tokens
    # ----------------------------------------------------------------------
    # Operator precedence table.   Operators must follow the same
    # precedence rules as in Python.  Instructions to be given in the project.

    precedence = (
        ('left', 'PLUS', 'MINUS'),
    )

    @_('statements statement')
    def statements(self, p):               # Multiple statements
        p.statements.append(p.statement)   # Add a statement to previous statements
        return p.statements

    @_('statement')
    def statements(self, p):               # A single statement
        # lineno are broken here because statements don't really have a line...
        return Statements([p.statement], lineno=p.statement.lineno)

    @_('var_declaration')
    def statement(self, p):
        return p[0]

    @_('expression PLUS expression')
    def expression(self, p):
        # I may want to map things like '<=' to 'LT'...
        return BinOp(p[1], p.expression0, p.expression1, lineno=p.lineno)

    @_('PLUS expression',
       'MINUS expression')
    def expression(self, p):
        return UnaryOp(p[0], p[1], lineno=p.lineno)

    @_('literal TIMES ID')
    def expression(self, p):
        return BinOp(p[1], p[0], SimpleLocation(p[2], True, lineno=p.lineno), lineno=p.lineno)

    @_('literal TIMES LPAREN ID RPAREN')
    def expression(self, p):
        return BinOp(p[1], p[0], SimpleLocation(p.ID, False, lineno=p.lineno), lineno=p.lineno)

    @_('ID')
    def expression(self, p):
        return SimpleLocation(p.ID, True, lineno=p.lineno)

    @_('LPAREN ID RPAREN')
    def expression(self, p):
        return SimpleLocation(p.ID, False, lineno=p.lineno)

    @_('literal TIMES EXPOSURE')
    def expression(self, p):
        return BinOp(p[1], p[0], Exposure(p[2], True, lineno=p.lineno), lineno=p.lineno)

    @_('literal TIMES LPAREN EXPOSURE RPAREN')
    def expression(self, p):
        return BinOp(p[1], p[0], Exposure(p[3], False, lineno=p.lineno), lineno=p.lineno)

    @_('EXPOSURE')
    def expression(self, p):
        return Exposure(p[0], True, lineno=p.lineno)

    @_('LPAREN EXPOSURE RPAREN')
    def expression(self, p):
        return Exposure(p[1], False, lineno=p.lineno)

    @_('literal')
    def expression(self, p):
        return p.literal

    @_('FLOAT')
    def literal(self, p):
        return FloatLiteral(float(p.FLOAT), lineno=p.lineno)

    @_('ID ASSIGN expression SEMI')
    def var_declaration(self, p):
        return VarDeclaration(p.ID, True, p.expression, lineno=p.lineno)

    @_('LPAREN ID RPAREN ASSIGN expression SEMI')
    def var_declaration(self, p):
        return VarDeclaration(p.ID, False, p.expression, lineno=p.lineno)

    @_('EXPOSURE ASSIGN expression SEMI')
    def var_declaration(self, p):
        return VarDeclaration(p[0], True, p.expression, lineno=p.lineno)

    @_('LPAREN EXPOSURE RPAREN ASSIGN expression SEMI')
    def var_declaration(self, p):
        return VarDeclaration(p[1], False, p.expression, lineno=p.lineno)

    @_('OUTCOME')
    def expression(self, p):
        return Outcome(p[0], True, lineno=p.lineno)

    @_('OUTCOME ASSIGN expression SEMI')
    def var_declaration(self, p):
        return OutcomeDeclaration(p.expression, lineno=p.lineno)


    # ----------------------------------------------------------------------
    # DO NOT MODIFY
    #
    # catch-all error handling.   The following function gets called on any
    # bad input.  p is the offending token or None if end-of-file (EOF).
    def error(self, p):
        if p:
            error(p.lineno, "Syntax error in input at token '%s'" % p.value)
        else:
            error('EOF','Syntax error. No more input.')



# ----------------------------------------------------------------------
#                     DO NOT MODIFY ANYTHING BELOW HERE
# ----------------------------------------------------------------------

def parse(source):
    '''
    Parse source code into an AST. Return the top of the AST tree.
    '''
    lexer = DogLexer()
    parser = DogParser()
    ast = parser.parse(lexer.tokenize(source))
    return ast

def main():
    '''
    Main program. Used for testing.
    '''
    import sys

    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python3 -m gone.parser filename\n')
        raise SystemExit(1)

    # Parse and create the AST
    ast = parse(open(sys.argv[1]).read())
    # Output the resulting parse tree structure
    for depth, node in flatten(ast):
       print('%s: %s%s' % (getattr(node, 'lineno', None), ' '*(4*depth), node))

if __name__ == '__main__':
    main()
