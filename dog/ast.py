# ast.py

class AST(object):
    _nodes = { }

    @classmethod
    def __init_subclass__(cls):
        AST._nodes[cls.__name__] = cls

        if not hasattr(cls, '__annotations__'):
            return

        fields = list(cls.__annotations__.items())

        def __init__(self, *args, **kwargs):
            if len(args) != len(fields):
                raise TypeError(f'Expected {len(fields)} arguments')
            for (name, ty), arg in zip(fields, args):
                if isinstance(ty, list):
                    if not isinstance(arg, list):
                        raise TypeError(f'{name} must be list')
                    if not all(isinstance(item, ty[0]) for item in arg):
                        raise TypeError(f'All items of {name} must be {ty[0]}')
                elif not isinstance(arg, ty):
                    raise TypeError(f'{name} must be {ty}, not {type(arg)}')
                setattr(self, name, arg)

            for name, val in kwargs.items():
                setattr(self, name, val)

        cls.__init__ = __init__
        cls._fields = [name for name,_ in fields]

    def __repr__(self):
        vals = [ getattr(self, name) for name in self._fields ]
        argstr = ', '.join(f'{name}={type(val).__name__ if isinstance(val, AST) else repr(val)}'
                           for name, val in zip(self._fields, vals))
        return f'{type(self).__name__}({argstr})'

# Abstract AST nodes
class Expression(AST):
    pass

class Statement(AST):
    pass

class Statements(AST):
    statements : [Statement]

    def __init__(self, statements):
        self.statements = statements

    def append(self, v):
        self.statements.append(v)

class Location(Expression):
   pass

class SimpleLocation(Location):
    name : str


class Exposure(Location):
    name : str

class VarDeclaration(Statement):
    '''
    var name datatype [ = value ];
    '''
    name     : str
    value    : Expression

class OutcomeDeclaration(VarDeclaration):
    '''
    var name datatype [ = value ];
    '''
    value    : Expression


class Literal(Expression):
    '''
    Base class for a literal value such as 2, 2.5, or "two"
    '''

class FloatLiteral(Literal):
    value : float

class BinOp(Expression):
    '''
    A Binary operator such as 2 + 3 or x * y
    '''
    op    : str
    left  : Expression
    right : Expression

class UnaryOp(Expression):
    '''
    A Unary operator such as -x or +x
    '''
    op      : str
    operand : Expression


class NodeVisitor(object):
    '''
    Class for visiting nodes of the parse tree.  This is modeled after
    a similar class in the standard library ast.NodeVisitor.  For each
    node, the visit(node) method calls a method visit_NodeName(node)
    which should be implemented in subclasses.  The generic_visit() method
    is called for all nodes where there is no matching visit_NodeName() method.

    Here is a example of a visitor that examines binary operators:

        class VisitOps(NodeVisitor):
            visit_BinOp(self,node):
                print('Binary operator', node.op)
                self.visit(node.left)
                self.visit(node.right)
            visit_UnaryOp(self,node):
                print('Unary operator', node.op)
                self.visit(node.expr)

        tree = parse(txt)
        VisitOps().visit(tree)
    '''
    def visit(self, node):
        '''
        Execute a method of the form visit_NodeName(node) where
        NodeName is the name of the class of a particular node.
        '''
        if isinstance(node, list):
            for item in node:
                self.visit(item)
        elif isinstance(node, AST):
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            visitor(node)

    def generic_visit(self,node):
        '''
        Method executed if no applicable visit_ method can be found.
        This examines the node to see if it has _fields, is a list,
        or can be further traversed.
        '''
        for field in getattr(node, '_fields'):
            value = getattr(node, field, None)
            self.visit(value)

    @classmethod
    def __init_subclass__(cls):
        '''
        Sanity check. Make sure that visitor classes use the right names
        '''
        for key in vars(cls):
            if key.startswith('visit_'):
                assert key[6:] in globals(), f"{key} doesn't match any AST node"

# DO NOT MODIFY
def flatten(top):
    '''
    Flatten the entire parse tree into a list for the purposes of
    debugging and testing.  This returns a list of tuples of the
    form (depth, node) where depth is an integer representing the
    parse tree depth and node is the associated AST node.
    '''
    class Flattener(NodeVisitor):
        def __init__(self):
            self.depth = 0
            self.nodes = []
        def generic_visit(self, node):
            self.nodes.append((self.depth, node))
            self.depth += 1
            NodeVisitor.generic_visit(self, node)
            self.depth -= 1

    d = Flattener()
    d.visit(top)
    return d.nodes
