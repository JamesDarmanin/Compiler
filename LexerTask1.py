from enum import Enum

class TokenType(Enum):
    integer_literal = 1
    fullstop = 2
    float_literal = 3
    identifier = 4
    Underscore = 5
    Keyword = 6
    close_curly = 7
    open_curly = 8
    colon = 9
    semicolon = 10
    comma = 11
    open_bracket = 12
    close_bracket = 13
    open_par = 14
    close_par = 15
    open_square_bracket = 16
    close_square_bracket = 17
    AdditiveOp = 18
    MultiplicativeOp = 19
    RelationalOp = 20
    whitespace = 21
    type = 22
    equal = 23
    bool = 24
    comment = 25
    hashtag = 26
    then = 27
    if_keyword = 28
    while_keyword = 29
    do = 30
    return_keyword = 31
    else_keyword = 32
    void = 33
    end = 34

class Token:
    def __init__(self, t, l):
        self.type = t
        self.lexeme = l

class Lexer:
    def __init__(self):
        self.lexeme_list = ["letter", "digit", "ws", "bool", "int", "float", "char", "fun", "equal", "true", "false", "colour", "hex", "close_curly", "open_curly", "colon", "semicolon", "comma",
                            "open_bracket", "close_bracket", "open_par", "fullstop", "close_par", "else", "for", "if", "return",
                            "while", "let", "line_comment", "__height", "__width", "__read", "__print", "__delay", "__random_int", "greater_then",
                            "smaller_then", "greater_or_equal_to", "smaller_or_equal_to", "not_equal_to", "equal_to", "plus", "minus", "or", "multiplication",
                            "division", "and", ".", "Underscore", "Double_Underscore", "open_square_bracket", "close_square_bracket", "type", "exclamation_mark", "as", "equals", "hashtag"]

        self.states_list = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
        self.states_accp = [1, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 28, 27, 29, 30, 31, 32, 33, 34, 35]

        self.rows = len(self.states_list)
        self.cols = len(self.lexeme_list)

        self.Tx = [[-1 for j in range(self.cols)] for i in range(self.rows)]
        self.InitializeTxTable()

    def InitializeTxTable(self):
        # Update Tx to represent the state transition function of the DFA
        # Variables

        # State 1
        self.Tx[0][self.lexeme_list.index("digit")] = 1
        self.Tx[1][self.lexeme_list.index("digit")] = 1

        # State 2
        self.Tx[1][self.lexeme_list.index("fullstop")] = 2

        # State 3
        self.Tx[2][self.lexeme_list.index("digit")] = 3
        self.Tx[3][self.lexeme_list.index("digit")] = 3

        # State 4
        self.Tx[0][self.lexeme_list.index("letter")] = 4
        self.Tx[4][self.lexeme_list.index("letter")] = 4

        # State 5
        self.Tx[0][self.lexeme_list.index("Underscore")] = 5

        # State 6
        self.Tx[5][self.lexeme_list.index("Underscore")] = 6

        #State 7
        self.Tx[6][self.lexeme_list.index("letter")] = 7
        self.Tx[7][self.lexeme_list.index("letter")] = 7
        self.Tx[7][self.lexeme_list.index("Underscore")] = 7

        # State 8
        self.Tx[0][self.lexeme_list.index("open_curly")] = 8

        # State 9
        self.Tx[0][self.lexeme_list.index("close_curly")] = 9

        # State 10
        self.Tx[0][self.lexeme_list.index("colon")] = 10

        # State 11
        self.Tx[0][self.lexeme_list.index("semicolon")] = 11

        # State 12
        self.Tx[0][self.lexeme_list.index("comma")] = 12

        # State 13
        self.Tx[0][self.lexeme_list.index("open_bracket")] = 13

        # State 14
        self.Tx[0][self.lexeme_list.index("close_bracket")] = 14

        # State 15
        self.Tx[0][self.lexeme_list.index("open_par")] = 15

        # State 16
        self.Tx[0][self.lexeme_list.index("close_par")] = 16

        # State 17
        self.Tx[0][self.lexeme_list.index("open_square_bracket")] = 17

        # State 18
        self.Tx[0][self.lexeme_list.index("close_square_bracket")] = 18

        # State 19
        self.Tx[0][self.lexeme_list.index("ws")] = 19
        self.Tx[19][self.lexeme_list.index("ws")] = 19

        # State 20
        self.Tx[0][self.lexeme_list.index("multiplication")] = 20

        # State 21
        self.Tx[0][self.lexeme_list.index("division")] = 21
        self.Tx[21][self.lexeme_list.index("digit")] = 21

        # State 33
        self.Tx[21][self.lexeme_list.index("division")] = 33
        self.Tx[33][self.lexeme_list.index("digit")] = 33
        self.Tx[33][self.lexeme_list.index("letter")] = 33

        # State 22
        self.Tx[0][self.lexeme_list.index("plus")] = 22

        # State 23
        self.Tx[0][self.lexeme_list.index("minus")] = 23
        self.Tx[23][self.lexeme_list.index("digit")] = 23

        # State 32
        self.Tx[23][self.lexeme_list.index("greater_then")] = 32
        self.Tx[32][self.lexeme_list.index("digit")] = 32

        # State 24
        self.Tx[0][self.lexeme_list.index("greater_then")] = 24
        self.Tx[24][self.lexeme_list.index("digit")] = 24

        # State 30
        self.Tx[24][self.lexeme_list.index("equals")] = 30
        self.Tx[30][self.lexeme_list.index("digit")] = 30

        # State 25
        self.Tx[0][self.lexeme_list.index("smaller_then")] = 25
        self.Tx[25][self.lexeme_list.index("digit")] = 25

        # State 31
        self.Tx[25][self.lexeme_list.index("equals")] = 31
        self.Tx[31][self.lexeme_list.index("digit")] = 31

        # State 26
        self.Tx[0][self.lexeme_list.index("exclamation_mark")] = 26

        # State 29
        self.Tx[26][self.lexeme_list.index("equals")] = 29
        self.Tx[29][self.lexeme_list.index("digit")] = 29

        # State 27
        self.Tx[0][self.lexeme_list.index("equals")] = 27
        self.Tx[27][self.lexeme_list.index("digit")] = 27

        #State 28
        self.Tx[27][self.lexeme_list.index("equals")] = 28
        self.Tx[28][self.lexeme_list.index("digit")] = 28



    def AcceptingStates(self, state):
        try:
            self.states_accp.index(state)
            return True
        except ValueError:
            return False

    def GetTokenTypeByFinalState(self, state, lexeme):
        if state == 1:
            return Token(TokenType.integer_literal, lexeme)
        elif state == 3:
            return Token(TokenType.float_literal, lexeme)
        elif state == 4:
            if lexeme == "int" : return Token(TokenType.type, lexeme)
            if lexeme in ["bool"]: return Token(TokenType.type, lexeme)
            if lexeme in ["char"]: return Token(TokenType.type, lexeme)
            if lexeme in ["fun"]: return Token(TokenType.type, lexeme)
            if lexeme in ["float"]: return Token(TokenType.type, lexeme)
            if lexeme in ["colour"]: return Token(TokenType.type, lexeme)
            if lexeme in ["or"]: return Token(TokenType.MultiplicativeOp, lexeme)
            if lexeme in ["for"]: return Token(TokenType.Keyword, lexeme)
            if lexeme in ["if"]: return Token(TokenType.Keyword, lexeme)
            if lexeme in ["while"]: return Token(TokenType.Keyword, lexeme)
            if lexeme in ["for"]: return Token(TokenType.Keyword, lexeme)
            if lexeme in ["return"]: return Token(TokenType.Keyword, lexeme)
            if lexeme in ["else"]: return Token(TokenType.Keyword, lexeme)
            if lexeme in ["let"]: return Token(TokenType.Keyword, lexeme)
            if lexeme in ["as"]: return Token(TokenType.Keyword, lexeme)
            if lexeme in ["true"]: return Token(TokenType.bool, lexeme)
            if lexeme in ["false"]: return Token(TokenType.bool, lexeme)
            return Token(TokenType.identifier, lexeme)
        elif state == 7:
            if lexeme in ["__width"] : return Token(TokenType.Keyword, lexeme)
            if lexeme in ["__height"]: return Token(TokenType.Keyword, lexeme)
            if lexeme in ["__read"]: return Token(TokenType.Keyword, lexeme)
            if lexeme in ["__random_int"]: return Token(TokenType.Keyword, lexeme)
            if lexeme in ["__print"]: return Token(TokenType.Keyword, lexeme)
            if lexeme in ["__delay"]: return Token(TokenType.Keyword, lexeme)
            if lexeme in ["__write_box"]: return Token(TokenType.Keyword, lexeme)
            if lexeme in ["__write"]: return Token(TokenType.Keyword, lexeme)
            return Token(TokenType.void, lexeme)
        elif state == 8:
            return Token(TokenType.open_curly, lexeme)
        elif state == 9:
            return Token(TokenType.close_curly, lexeme)
        elif state == 10:
            return Token(TokenType.colon, lexeme)
        elif state == 11:
            return Token(TokenType.semicolon, lexeme)
        elif state == 12:
            return Token(TokenType.comma, lexeme)
        elif state == 13:
            return Token(TokenType.open_bracket, lexeme)
        elif state == 14:
            return Token(TokenType.close_bracket, lexeme)
        elif state == 15:
            return Token(TokenType.open_par, lexeme)
        elif state == 16:
            return Token(TokenType.close_par, lexeme)
        elif state == 17:
            return Token(TokenType.open_square_bracket, lexeme)
        elif state == 18:
            return Token(TokenType.close_square_bracket, lexeme)
        elif state == 19:
            return Token(TokenType.whitespace, lexeme)
        elif state == 20:
            return Token(TokenType.MultiplicativeOp, lexeme)
        elif state == 21:
            return Token(TokenType.MultiplicativeOp, lexeme)
        elif state == 22:
            return Token(TokenType.AdditiveOp, lexeme)
        elif state == 23:
            return Token(TokenType.AdditiveOp, lexeme)
        elif state == 24:
            return Token(TokenType.RelationalOp, lexeme)
        elif state == 25:
            return Token(TokenType.RelationalOp, lexeme)
        elif state == 28:
            return Token(TokenType.RelationalOp, lexeme)
        elif state == 27:
            return Token(TokenType.RelationalOp, lexeme)
        elif state == 29:
            return Token(TokenType.RelationalOp, lexeme)
        elif state == 30:
            return Token(TokenType.RelationalOp, lexeme)
        elif state == 31:
            return Token(TokenType.RelationalOp, lexeme)
        elif state == 32:
            return Token(TokenType.RelationalOp, lexeme)
        elif state == 33:
            return Token(TokenType.comment, lexeme)
        elif state == 34:
            return Token(TokenType.RelationalOp, lexeme)
        else:
            return Token(TokenType.void, lexeme)

    def CatChar(self, character, state=None):
        cat = "other"
        if character.isalpha():
            cat = "letter"
        if character.isdigit():
            cat = "digit"
        if character == ".":
            cat = "fullstop"
        if character == "_":
            cat = "Underscore"
        if character == " ":
            cat = "ws"
        if character == ";":
            cat = "semicolon"
        if character == ":":
            cat = "colon"
        if character == ",":
            cat = "comma"
        if character == ">":
            cat = "greater_then"
        if character == "<":
            cat = "smaller_then"
        if character == "=":
            cat = "equals"
        if character == "+":
            cat = "plus"
        if character == "-":
            cat = "minus"
        if character == "*":
            cat = "multiplication"
        if character == "/":
            cat = "division"
        if character == ")":
            cat = "close_bracket"
        if character == "(":
            cat = "open_bracket"
        if character == "{":
            cat = "open_curly"
        if character == "}":
            cat = "close_curly"
        if character == "[":
            cat = "open_square_bracket"
        if character == "]":
            cat = "close_square_bracket"
        if character == "!":
            cat = "exclamation_mark"
        return cat

    def EndOfInput(self, src_program_str, src_program_idx):
        if src_program_idx > len(src_program_str) - 1:
            return True
        else:
            return False

    def NextChar(self, src_program_str, src_program_idx):
        if not self.EndOfInput(src_program_str, src_program_idx):
            return True, src_program_str[src_program_idx]
        else:
            return False, "."

    def NextToken(self, src_program_str, src_program_idx):
        state = 0  # initial state is 0 - check Tx
        stack = []
        lexeme = ""
        stack.append(-2)  # insert the error state at the bottom of the stack.

        while state != -1:
            if self.AcceptingStates(state):
                stack.clear()
            stack.append(state)

            exists, character = self.NextChar(src_program_str, src_program_idx)
            lexeme += character
            if not exists:
                break  # Break out of loop if we're at the end of the string
            src_program_idx += 1

            cat = self.CatChar(character)
            state = self.Tx[state][self.lexeme_list.index(cat)]

        lexeme = lexeme[:-1]  # remove the last character added which sent the lexer to state -1

        syntax_error = False
        # rollback
        while len(stack) > 0:
            if stack[-1] == -2:  # report a syntax error
                syntax_error = True
                exists, character = self.NextChar(src_program_str, src_program_idx - 1)
                lexeme = character
                break

            # Pop this state if not an accepting state.
            if not self.AcceptingStates(stack[-1]):
                stack.pop()
                lexeme = lexeme[:-1]

            # This is an accepting state ... return it.
            else:
                state = stack.pop()
                break

        if syntax_error:
            return Token(TokenType.void, lexeme), "error"

        if self.AcceptingStates(state):
            return self.GetTokenTypeByFinalState(state, lexeme), lexeme
        else:
            return Token(TokenType.void, lexeme), "Lexical Error"

    def GenerateTokens(self, src_program_str):
        tokens_list = []
        src_program_idx = 0
        token, lexeme = self.NextToken(src_program_str, src_program_idx)
        tokens_list.append(token)

        while token != -1:
            src_program_idx += len(lexeme)
            if not self.EndOfInput(src_program_str, src_program_idx):
                token, lexeme = self.NextToken(src_program_str, src_program_idx)
                tokens_list.append(token)
                if token.type == TokenType.void:
                    break  # A lexical error was encountered
            else:
                break  # The end of the source program

        return tokens_list

    def GenerateTokensFromFile(self, file_path):
        with open(file_path, 'r') as file:
            src_program_str = file.read()
        return self.GenerateTokens(src_program_str)

lex = Lexer()
toks = lex.GenerateTokensFromFile("ExampleForTasks")
for t in toks:
    print(t.type, t.lexeme)




