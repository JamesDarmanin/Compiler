import LexerTask1 as lex
import astnodes as ast

class Parser:
    def __init__(self, file_path):
        self.lexer = lex.Lexer()
        self.tokens = self.lexer.GenerateTokensFromFile(file_path)
        self.idx = -1

    def next_token(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            return self.tokens[self.idx]
        else:
            return lex.Token(lex.TokenType.end, "")

    def peek_token(self):
        next_idx = self.idx + 1
        if next_idx < len(self.tokens):
            return self.tokens[next_idx]
        else:
            return lex.Token(lex.TokenType.end, "")

    def consume_token(self):
        self.idx += 1

    def parse_primary_expression(self):
        token = self.next_token()
        if token.type in [lex.TokenType.integer_literal, lex.TokenType.float_literal]:
            self.consume_token()
            return ast.ASTIntegerNode(token.lexeme)  # Handle float if necessary
        elif token.type == lex.TokenType.identifier:
            self.consume_token()
            return ast.ASTVariableNode(token.lexeme)
        elif token.type == lex.TokenType.open_par:
            expr = self.parse_expression()
            if self.peek_token().type == lex.TokenType.close_par:
                self.consume_token()
                return expr
            else:
                print("Syntax Error: Missing closing parenthesis")
                return None
        else:
            print("Syntax Error: Unexpected token in primary expression")
            return None

    def parse_factor(self):
        left_expr = self.parse_primary_expression()
        while self.peek_token().type in [lex.TokenType.MultiplicativeOp]:
            operator = self.next_token().lexeme
            self.consume_token()
            right_expr = self.parse_primary_expression()
            left_expr = ast.ASTBinaryOperationNode(operator, left_expr, right_expr)
        return left_expr

    def parse_term(self):
        left_expr = self.parse_factor()
        while self.peek_token().type in [lex.TokenType.AdditiveOp]:
            operator = self.next_token().lexeme
            self.consume_token()
            right_expr = self.parse_factor()
            left_expr = ast.ASTBinaryOperationNode(operator, left_expr, right_expr)
        return left_expr

    def parse_comparison(self):
        left_expr = self.parse_term()
        while self.peek_token().type in [lex.TokenType.RelationalOp]:
            operator = self.next_token().lexeme
            self.consume_token()
            right_expr = self.parse_term()
            left_expr = ast.ASTBinaryOperationNode(operator, left_expr, right_expr)
        return left_expr

    def parse_expression(self):
        return self.parse_comparison()

    def parse_assignment(self):
        initial_token = self.next_token()

        if initial_token.type != lex.TokenType.identifier:
            print("Syntax Error: Identifier expected for assignment")
            return None

        assignment_lhs = ast.ASTVariableNode(initial_token.lexeme)
        self.consume_token()

        if self.next_token().type != lex.TokenType.equal:
            print("Syntax Error: '=' expected after identifier")
            return None
        self.consume_token()

        assignment_rhs = self.parse_expression()
        if assignment_rhs is None:
            print("Syntax Error: Invalid expression in assignment")
            return None

        # Handle type checking or conversion if necessary
        if isinstance(assignment_lhs, ast.ASTVariableNode) and initial_token.lexeme.startswith('int'):
            if isinstance(assignment_rhs, ast.ASTFloatNode):
                print("Type Warning: Converting float to int for assignment")
                assignment_rhs = ast.ASTIntegerNode(int(float(assignment_rhs.value)))
            elif not isinstance(assignment_rhs, ast.ASTIntegerNode):
                print("Type Error: Expected integer value for int variable")
                return None

        return ast.ASTAssignmentNode(assignment_lhs, assignment_rhs)

    def parse_if_statement(self):
        self.consume_token()  # Consume 'if'
        condition = self.parse_expression()
        if self.next_token().type != lex.TokenType.then:
            print("Syntax Error: 'then' expected")
            return None
        self.consume_token()  # Consume 'then'
        then_block = self.parse_block()

        else_block = None
        if self.next_token().type == lex.TokenType.else_keyword:
            self.consume_token()  # Consume 'else'
            else_block = self.parse_block()

        return ast.ASTIfNode(condition, then_block, else_block)

    def parse_while_statement(self):
        self.consume_token()  # Consume 'while'
        condition = self.parse_expression()
        if self.next_token().type != lex.TokenType.do:
            print("Syntax Error: 'do' expected")
            return None
        self.consume_token()  # Consume 'do'
        body = self.parse_block()
        return ast.ASTWhileNode(condition, body)

    def parse_return_statement(self):
        self.consume_token()  # Consume 'return'
        expression = self.parse_expression()  # Parse the expression to return
        if expression is None:
            print("Syntax Error: Invalid expression in return statement")
            return None
        return ast.ASTReturnNode(expression)  # Return a node representing the return statement

    def parse_statement(self):
        next_token = self.peek_token()  # Look at the next token to decide the parsing strategy
        if next_token.type == lex.TokenType.if_keyword:
            self.consume_token()  # consume 'if'
            return self.parse_if_statement()
        elif next_token.type == lex.TokenType.while_keyword:
            self.consume_token()  # consume 'while'
            return self.parse_while_statement()
        elif next_token.type == lex.TokenType.return_keyword:
            self.consume_token()  # consume 'return'
            return self.parse_return_statement()
        elif next_token.type == lex.TokenType.identifier:
            return self.parse_assignment()
        else:
            print("Syntax Error: Unexpected token in statement")
            return None

    def parse_block(self):
        block = ast.ASTBlockNode()
        while self.idx < len(self.tokens) and self.tokens[self.idx].type != lex.TokenType.end:
            statement = self.parse_statement()
            if statement:
                block.add_statement(statement)
                if self.next_token().type == lex.TokenType.semicolon:
                    self.consume_token()
                else:
                    print("Syntax Error: Missing semicolon")
                    break
        return block

    def parse_program(self):
        self.consume_token()  # Move to the first token
        return self.parse_block()

    def parse(self):
        return self.parse_program()

    # Usage
file_path = "ExampleForTasks"
parser = Parser(file_path)
ast_root = parser.parse()

# Printing the AST
print_visitor = ast.PrintNodesVisitor()
ast_root.accept(print_visitor)
