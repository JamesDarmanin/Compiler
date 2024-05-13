# Base classes for AST nodes
class ASTNode:
    def __init__(self):
        self.name = "ASTNode"


class ASTStatementNode(ASTNode):
    def __init__(self):
        super().__init__()
        self.name = "ASTStatementNode"


class ASTExpressionNode(ASTNode):
    def __init__(self):
        super().__init__()
        self.name = "ASTExpressionNode"


class ASTFunctionCallNode(ASTExpressionNode):
    def init(self, function_name, arguments):
        super().init()
        self.function_name = function_name
        self.arguments = arguments

    def accept(self, visitor):
        visitor.visit_function_call_node(self)


class ASTGroupingNode(ASTExpressionNode):
    def init(self, expression):
        super().init()
        self.expression = expression

    def accept(self, visitor):
        visitor.visit_grouping_node(self)


# Concrete AST node classes
class ASTVariableNode(ASTExpressionNode):
    def __init__(self, lexeme):
        super().__init__()
        self.name = "ASTVariableNode"
        self.lexeme = lexeme

    def accept(self, visitor):
        visitor.visit_variable_node(self)


class ASTIntegerNode(ASTExpressionNode):
    def __init__(self, value):
        super().__init__()
        self.name = "ASTIntegerNode"
        self.value = value

    def accept(self, visitor):
        visitor.visit_integer_node(self)


class ASTAssignmentNode(ASTStatementNode):
    def __init__(self, variable, expression):
        super().__init__()
        self.name = "ASTAssignmentNode"
        self.variable = variable
        self.expression = expression

    def accept(self, visitor):
        visitor.visit_assignment_node(self)


class ASTBlockNode(ASTNode):
    def __init__(self):
        super().__init__()
        self.name = "ASTBlockNode"
        self.statements = []

    def add_statement(self, node):
        self.statements.append(node)

    def accept(self, visitor):
        visitor.visit_block_node(self)


class ASTIfNode(ASTStatementNode):
    def __init__(self, condition, true_branch):
        super().__init__()
        self.name = "ASTIfNode"
        self.condition = condition
        self.true_branch = true_branch

    def accept(self, visitor):
        visitor.visit_if_node(self)


class ASTWhileNode(ASTStatementNode):
    def __init__(self, condition, body):
        super().__init__()
        self.name = "ASTWhileNode"
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        visitor.visit_while_node(self)


class ASTForNode(ASTStatementNode):
    def __init__(self, condition, body):
        super().__init__()
        self.name = "ASTForNode"
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        visitor.visit_for_node(self)


class ASTReturnNode(ASTStatementNode):
    def __init__(self, condition, body):
        super().__init__()
        self.name = "ASTReturnNode"
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        visitor.visit_return_node(self)


class ASTElseNode(ASTStatementNode):
    def __init__(self, condition, body):
        super().__init__()
        self.name = "ASTElseNode"
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        visitor.visit_else_node(self)


class ASTLetNode(ASTStatementNode):
    def __init__(self, condition, body):
        super().__init__()
        self.name = "ASTLetNode"
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        visitor.visit_let_node(self)


class ASTAsNode(ASTStatementNode):
    def __init__(self, condition, body):
        super().__init__()
        self.name = "ASTAsNode"
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        visitor.visit_as_node(self)


class ASTTypeDeclarationNode(ASTStatementNode):
    def __init__(self, type_name, variable_name, initializer=None):
        super().__init__()
        self.type_name = type_name
        self.variable_name = variable_name
        self.initializer = initializer  # This can be None if no initialization is provided

    def accept(self, visitor):
        visitor.visit_type_declaration_node(self)


# Visitor pattern base class
class ASTVisitor:
    def visit_integer_node(self, node):
        raise NotImplementedError

    def visit_assignment_node(self, node):
        raise NotImplementedError

    def visit_variable_node(self, node):
        raise NotImplementedError

    def visit_block_node(self, node):
        raise NotImplementedError

    def visit_if_node(self, node):
        raise NotImplementedError

    def visit_while_node(self, node):
        raise NotImplementedError

    def visit_for_node(self, node):
        raise NotImplementedError

    def visit_else_node(self, node):
        raise NotImplementedError

    def visit_return_node(self, node):
        raise NotImplementedError

    def visit_let_node(self, node):
        raise NotImplementedError

    def visit_as_node(self, node):
        raise NotImplementedError

    def visit_type_declaration_node(self, node):
        raise NotImplementedError

    def inc_tab_count(self):
        raise NotImplementedError

    def dec_tab_count(self):
        raise NotImplementedError


# A specific implementation of a visitor for printing the AST
class PrintNodesVisitor(ASTVisitor):
    def __init__(self):
        self.tab_count = 0

    def inc_tab_count(self):
        self.tab_count += 1

    def dec_tab_count(self):
        self.tab_count -= 1

    def visit_integer_node(self, node):
        print('\t' * self.tab_count + "Integer value:", node.value)

    def visit_assignment_node(self, node):
        print('\t' * self.tab_count + "Assignment node:")
        self.inc_tab_count()
        node.variable.accept(self)
        node.expression.accept(self)
        self.dec_tab_count()

    def visit_variable_node(self, node):
        print('\t' * self.tab_count + "Variable:", node.lexeme)

    def visit_block_node(self, node):
        print('\t' * self.tab_count + "New Block:")
        self.inc_tab_count()
        for statement in node.statements:
            statement.accept(self)
        self.dec_tab_count()

    def visit_if_node(self, node):
        print('\t' * self.tab_count + "If Node:")
        self.inc_tab_count()
        node.condition.accept(self)
        node.true_branch.accept(self)
        self.dec_tab_count()

    def visit_while_node(self, node):
        print('\t' * self.tab_count + "While Node:")
        self.inc_tab_count()
        node.condition.accept(self)
        node.body.accept(self)
        self.dec_tab_count()

    def visit_for_node(self, node):
        print('\t' * self.tab_count + "For Node:")
        self.inc_tab_count()
        node.condition.accept(self)
        node.body.accept(self)
        self.dec_tab_count()

    def visit_return_node(self, node):
        print('\t' * self.tab_count + "Return Node:")
        self.inc_tab_count()
        node.condition.accept(self)
        node.body.accept(self)
        self.dec_tab_count()

    def visit_type_declaration_node(self, node):
        print(f"{node.type_name} {node.variable_name}", end="")
        if node.initializer:
            print(" = ", end="")
            node.initializer.accept(self)
        print()


# Create a print visitor instance
print_visitor = PrintNodesVisitor()
