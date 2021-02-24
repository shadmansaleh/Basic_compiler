'''Code for basic class'''

from string_with_arrows import string_with_arrows


############
#  TOKENS  #
############

TT_INT    = 'TT_INT'
TT_FLOAT  = 'TT_FLOAT'
TT_PLUS   = 'PLUS'
TT_MINUS  = 'TT_MINUS'
TT_MUL    = 'TT_MUL'
TT_DIV    = 'TT_DIV'
TT_LPARAN = 'TT_LPARAN'
TT_RPARAN = 'TT_RPARAN'
TT_EOF    = 'TT_EOF'


#######################
#  CHARECTER CLASSES  #
#######################

IGNORE_LIST = " \t"
DIGITS = '0123456789'


class Error:
    def __init__(self, position_start, position_end, error_name:str, details):
        self.position_start = position_start
        self.position_end = position_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}:{self.details}\n'
        result += f'File: {self.position_start.fn}, Line:{self.position_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.position_start.ftext, self.position_start, self.position_end)
        return result
        # return self.details.text + '\n' + ' ' * self.details.pos + '^\n'+f"{self.error_name} Error: Unexpected '{self.details.current_char}' at {self.details.pos}\n"


class Illegal_char_error(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Invalid syntax', details)

class Token:
    def __init__(self, type:str, value=None, start_pos=None, end_pos=None):
        self.type  = type
        self.value = value
        if start_pos: 
            self.pos_start = start_pos.copy()
            self.pos_end = start_pos.copy()
            self.pos_end.advance()
        
        if end_pos: self.pos_end = end_pos.copy()

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


##############
#  POSITION  #
##############

class Position:
    def __init__(self, idx, ln, col, fn, ftext):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftext = ftext

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1
        if current_char == '\n':
            self.col = 0
            self.ln += 1
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftext)


#########
# LEXER #
#########

class Lexer:
    def __init__(self, fn, text:str):
        self.fn = fn
        self.text = text
        self.pos:Position = Position(-1, 0, -1, self.fn, self.text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens:list = []
        while self.current_char != None:
            if self.current_char in IGNORE_LIST:
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, start_pos=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, start_pos=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, start_pos=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, start_pos=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPARAN, start_pos=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPARAN, start_pos=self.pos))
                self.advance()
            else:
                char = self.current_char
                pos = self.pos.copy()
                self.advance()
                return [], Illegal_char_error(pos, self.pos,"'" + char + "'")

        tokens.append(Token(TT_EOF, start_pos=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count > 0: self.error()
                dot_count += 1
            num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def error(self):
        raise(ValueError(f'E{self.pos.col} Unexpected {self.current_char}\n' + self.text + '\n' + ' ' * self.pos.col + '^'))


############
#  NUMBER  #
############

class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'


#####################
#  BINARY OPERATOR  #
#####################

class BinaryOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f"({self.left_node},{self.op_tok},{self.right_node})"

class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

    def __repr__(self):
        return f"({self.op_tok},{self.node})"

######
#  Parse Result  #
######

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


######
#  PARSER  #
######

class Parser:
    def __init__(self, tokens:list):
        self.tokens = tokens
        self.idx = -1
        self.advance()

    def advance(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.current_token = self.tokens[self.idx]
            return self.current_token

    def parse(self):
        res = self.expr()
        if not res.error and self.current_token.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected '+', '-', '*' or '/'"))
        return res

    def factor(self):
        res = ParseResult()
        tok = self.current_token
        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        elif tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        elif tok.type == TT_LPARAN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_token.type == TT_RPARAN:
                res.register(self.advance())
                if res.error: return res
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected ')'"))

            
        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected an Int or a Float"))

    def term(self):
        return self.binary_ops(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        return self.binary_ops(self.term, (TT_PLUS, TT_MINUS))

    def binary_ops(self, fn, ops):
        res = ParseResult()
        left = res.register(fn())
        if res.error: return res

        while self.current_token.type in ops:
            op = self.current_token
            res.register(self.advance())
            right = res.register(fn())
            if res.error: return res
            left = BinaryOpNode(left, op, right)
        return res.success(left)



########
#  RUN #
########


def run(fn, text):
    # Genarate Tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Gnarate AST
    parser = Parser(tokens)
    ast = parser.parse()
    return ast.node, ast.error

