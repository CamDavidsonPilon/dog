
from .errors import error

# -----------------------------------------------------------------------
# The SLY package. https://github.com/dabeaz/sly
from sly import Lexer


class DogLexer(Lexer):

    tokens = {
        # keywords

        # Identifiers
        ID,

        # Literals
        FLOAT,

        # Operators
        PLUS, MINUS, TIMES, ASSIGN,

        # Other symbols
        SEMI, OUTCOME, EXPOSURE
    }


    # ----------------------------------------------------------------------
    # Ignored characters (whitespace)
    #
    # The following individual characters are ignored completely by the lexer
    # when they appear between tokens.  Do not change.
    ignore = ' \t\r'



    @_(r'//.*?\n')
    def ignore_line_comment(self,  t):
        self.lineno += t.value.count('\n')


    @_(r'/\*[\s\S]*?\*/\n')
    def ignore_block_comment(self,  t):
        self.lineno += t.value.count('\n')

    UNTERMINATED_BLOCK_COMMENT = r'/\*[\s\S]*[^\*/\n]'

    def UNTERMINATED_BLOCK_COMMENT(self, t):
        error(self.lineno,"Unterminated block comment")
        self.index += len(t.value)
        self.lineno += t.value.count('\n')
        return None

    # One or more newlines \n\n\n...
    @_(r'\n+')
    def ignore_newline(self,  t):
        self.lineno += t.value.count('\n')

    # this can be simplified
    FLOAT = r'-?(\d*\.\d*([eE][\+-]?\d*)?)|(\d+([eE][\+-]?\d*))'

    def FLOAT(self, t):
        if 'e' in t.value or 'E' in t.value:
            t.value = t.value.lower()
            base, power = t.value.split('e')
            t.value = float(base) * 10**int(power)
        return t

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'


    ASSIGN = r'~'

    SEMI = r';'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['E'] = EXPOSURE
    ID['O'] = OUTCOME


    def error(self, t):
        error(self.lineno,"Illegal character %r" % t.value[0])
        self.index += 1


def main():
    '''
    Main program. For debugging purposes.
    '''
    import sys

    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 -m dog.lexer filename\n")
        raise SystemExit(1)

    lexer = DogLexer()
    text = open(sys.argv[1]).read()
    for tok in lexer.tokenize(text):
        print(tok)

if __name__ == '__main__':
    main()
