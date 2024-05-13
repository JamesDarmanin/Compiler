import astnodes as ast
import LexerTask1 as lex

class Parser:
    def __init__(self, src_program_str):
        self.name = "PARSEAR"
        self.lexer = lex.Lexer()
        self.tokens = self.lexer.GenerateTokens(src_program_str)
        self.index = 0
        self.crtToken = self.tokens[0] if self.tokens else lex.Token(lex.TokenType.end, "END")

    def NextToken(self):
        # Skip whitespace automatically
        while True:
            self.index += 1
            if self.index < len(self.tokens):
                self.crtToken = self.tokens[self.index]
                if self.crtToken.type != lex.TokenType.whitespace:
                    break
            else:
                self.crtToken = lex.Token(lex.TokenType.end, "END")
                break

    def ParseExpression(self):
        if self.crtToken.type == lex.TokenType.integer_literal:
            value = self.crtToken.lexeme
            self.NextToken()
            return ast.ASTIntegerNode(value)
        # Extend this method to handle more complex expressions

    def ParseAssignment(self):
        assignment_lhs = ast.ASTVariableNode(self.crtToken.lexeme)
        self.NextToken()  # consume the identifier
        if self.crtToken.type != lex.TokenType.equal:
            raise SyntaxError("Expected '=' in assignment")
        self.NextToken()  # consume '='
        assignment_rhs = self.ParseExpression()  # parse the right-hand side expression
        return ast.ASTAssignmentNode(assignment_lhs, assignment_rhs)

    def ParseTypeDeclaration(self):
        # Assuming the current token is the type
        type_name = self.crtToken.lexeme  # 'int', 'float', etc.
        self.NextToken()  # Move to the next token, which should be the identifier (variable name)

        if self.crtToken.type != lex.TokenType.identifier:
            raise SyntaxError("Expected identifier after type name")

        variable_name = self.crtToken.lexeme
        self.NextToken()  # Move past the variable name

        # Check if there is an initialization
        initializer = None
        if self.crtToken.type == lex.TokenType.equal:
            self.NextToken()  # Consume the '='
            initializer = self.ParseExpression()  # Parse the initialization expression

        # Create a type declaration node
        return ast.ASTTypeDeclarationNode(type_name, variable_name, initializer)

    def ParseIfStatement(self):
        self.NextToken()  # consume 'if'
        condition = self.ParseExpression()  # Directly parse the condition
        true_branch = self.ParseStatement()  # Parse the statement that executes if the condition is true
        return ast.ASTIfNode(condition, true_branch)

    def ParseWhileStatement(self):
        self.NextToken()  # consume 'while'
        condition = self.ParseExpression()  # Directly parse the condition
        body = self.ParseStatement()  # Parse the body of the while loop
        return ast.ASTWhileNode(condition, body)

    def ParseForStatement(self):
        self.NextToken()  # consume 'for'
        condition = self.ParseExpression()  # Directly parse the condition
        body = self.ParseStatement()  # Parse the body of the loop
        return ast.ASTForNode(condition, body)

    def ParseReturnStatement(self):
        self.NextToken()  # consume 'return'
        expression = self.ParseExpression()  # Directly parse the expression to return
        return ast.ASTReturnNode(expression)

    def ParseElseStatement(self):
        self.NextToken()  # consume 'else'
        body = self.ParseStatement()  # Directly parse the else body
        return ast.ASTElseNode(body)

    def ParseLetStatement(self):
        self.NextToken()  # consume 'let'
        identifier = self.ParseExpression()  # Assume the first expression is an identifier or similar
        body = self.ParseStatement()  # Parse the statement to execute
        return ast.ASTLetNode(identifier, body)

    def ParseAsStatement(self):
        self.NextToken()  # consume 'as'
        identifier = self.ParseExpression()  # Assume the first expression is an identifier or similar
        body = self.ParseStatement()  # Parse the body that follows
        return ast.ASTAsNode(identifier, body)

    def ParseStatement(self):
        if self.crtToken.type == lex.TokenType.Keyword:
            if self.crtToken.lexeme == "if":
                return self.ParseIfStatement()
            elif self.crtToken.lexeme == "while":
                return self.ParseWhileStatement()
            elif self.crtToken.lexeme == "for":
                return self.ParseForStatement()
            elif self.crtToken.lexeme == "return":
                return self.ParseReturnStatement()
            elif self.crtToken.lexeme == "else":
                return self.ParseElseStatement()
            elif self.crtToken.lexeme == "let":
                return self.ParseLetStatement()
            elif self.crtToken.lexeme == "as":
                return self.ParseAsStatement()
            else:
                raise SyntaxError(f"Syntax Error: Unrecognized keyword '{self.crtToken.lexeme}'")
        elif self.crtToken.type == lex.TokenType.open_par:
            return self.ParseAssignment()
        elif self.crtToken.type == lex.TokenType.close_par:
            return self.ParseAssignment()
        elif self.crtToken.type == lex.TokenType.open_bracket:
            return self.ParseAssignment()
        elif self.crtToken.type == lex.TokenType.close_bracket:
            return self.ParseAssignment()
        elif self.crtToken.type == lex.TokenType.open_square_bracket:
            return self.ParseAssignment()
        elif self.crtToken.type == lex.TokenType.close_square_bracket:
            return self.ParseAssignment()
        elif self.crtToken.type == lex.TokenType.open_curly:
            return self.ParseAssignment()
        elif self.crtToken.type == lex.TokenType.close_curly:
            return self.ParseAssignment()
        elif self.crtToken.type == lex.TokenType.comma:
            return self.ParseAssignment()
        elif self.crtToken.type == lex.TokenType.colon:
            return self.ParseAssignment()
        elif self.crtToken.type == lex.TokenType.semicolon:
            return self.ParseAssignment()
        elif self.crtToken.type == lex.TokenType.AdditiveOp:
            return self.ParseAssignment()
        elif self.crtToken.type == lex.TokenType.MultiplicativeOp:
            return self.ParseAssignment()
        elif self.crtToken.type == lex.TokenType.RelationalOp:
            return self.ParseAssignment()
        elif self.crtToken.type == lex.TokenType.identifier:
            return self.ParseAssignment()
        else:
            raise SyntaxError("Syntax Error: Unrecognized statement start")

    def ParseBlock(self):
        block = ast.ASTBlockNode()
        while self.crtToken.type != lex.TokenType.end and self.crtToken.type != lex.TokenType.close_curly:
            statement = self.ParseStatement()
            block.add_statement(statement)
            if self.crtToken.type == lex.TokenType.semicolon:
                self.NextToken()
            else:
                raise SyntaxError("Expected ';' after statement")
        return block

    def ParseProgram(self):
        return self.ParseBlock()

    def Parse(self):
        self.ParseProgram()  # start the parsing process

# Assuming the correct setup of lexer and AST nodes
parser = Parser("int")
parser.Parse()

print_visitor = ast.PrintNodesVisitor()
parser.ASTroot.accept(print_visitor)
