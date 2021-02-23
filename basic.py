'''Code for basic class'''

############
#  TOKENS  #
############

TT_INT    = 'TT_INT'
TT_FLOAT  = 'TT_FLOAT'
TT_PLUS   = 'PLUS'
TT_MINUS  = 'TT_MINUS'
TT_MUL    = 'TT_MUL'
TT_DIV    = 'TR_DIV'
TT_LPARAN = 'TT_LPARAN'
TT_RPARAN = 'TT_RPARAN'


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
        return result
        # return self.details.text + '\n' + ' ' * self.details.pos + '^\n'+f"{self.error_name} Error: Unexpected '{self.details.current_char}' at {self.details.pos}\n"


class Illegal_char_error(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class Token:
    def __init__(self, type:str, value=None):
        self.type  = type
        self.value = value

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

    def advance(self, current_char):
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
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPARAN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPARAN))
                self.advance()
            else:
                char = self.current_char
                pos = self.pos.copy()
                self.advance()
                return [], Illegal_char_error(pos, self.pos,"'" + char + "'")

        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count > 0: self.error()
                dot_count += 1
            num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))

    def error(self):
        raise(ValueError(f'E{self.pos.col} Unexpected {self.current_char}\n' + self.text + '\n' + ' ' * self.pos.col + '^'))


########
#  RUN #
########


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    return tokens, error
