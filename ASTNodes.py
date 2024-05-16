# First some AST Node classes we'll use to build the AST with
class ASTNode:
    def __init__(self):
        self.name = "ASTNode"


class ASTStatementNode(ASTNode):
    def __init__(self):
        self.name = "ASTStatementNode"


class ASTExpressionNode(ASTNode):
    def __init__(self):
        self.name = "ASTExpressionNode"


class ASTBooleanLiteralNode(ASTExpressionNode):
    def __init__(self, value):
        super().__init__()
        self.name = "ASTBooleanLiteralNode"
        self.value = bool(value)  # Ensure the value is a boolean

    def accept(self, visitor):
        visitor.visit_boolean_literal_node(self)


class ASTIntegerNode(ASTExpressionNode):
    def __init__(self, v):
        super().__init__()
        self.name = "ASTIntegerNode"
        self.value = v

    def accept(self, visitor):
        visitor.visit_integer_node(self)


class ASTFloatLiteralNode(ASTExpressionNode):
    def __init__(self, value):
        super().__init__()
        self.name = "ASTFloatLiteralNode"
        self.value = float(value)  # Ensure the value is a float

    def accept(self, visitor):
        visitor.visit_float_literal_node(self)


class ASTTypeNode(ASTNode):
    def __init__(self, type_name):
        super().__init__()
        self.name = "ASTTypeNode"
        self.type_name = type_name  # Ensure the type_name is one of 'float', 'int', 'bool', 'colour'

    def accept(self, visitor):
        visitor.visit_type_node(self)


class ASTVariableNode(ASTExpressionNode):
    def __init__(self, lexeme):
        super().__init__()
        self.name = "ASTVariableNode"
        self.lexeme = lexeme

    def accept(self, visitor):
        visitor.visit_variable_node(self)


class ASTAssignmentNode(ASTStatementNode):
    def __init__(self, ast_var_node, ast_expression_node):
        super().__init__()
        self.name = "ASTStatementNode"
        self.id = ast_var_node
        self.expr = ast_expression_node

    def accept(self, visitor):
        visitor.visit_assignment_node(self)


class ASTBlockNode(ASTStatementNode):
    def __init__(self, statements=None):
        super().__init__()
        self.name = "ASTBlockNode"
        self.statements = statements if statements else []

    def add_statement(self, statement):
        self.statements.append(statement)

    def accept(self, visitor):
        visitor.visit_block_node(self)


class ASTColourLiteralNode(ASTExpressionNode):
    def __init__(self, value):
        super().__init__()
        self.name = "ASTColourLiteralNode"
        self.value = value  # The value should be a hex colour code

    def accept(self, visitor):
        visitor.visit_colour_literal_node(self)


class ASTFunctionInvocationNode(ASTExpressionNode):
    def __init__(self, function_name, arguments):
        super().__init__()
        self.name = "ASTFunctionInvocationNode"
        self.function_name = function_name
        self.arguments = arguments  # List of ASTExpressionNode

    def accept(self, visitor):
        visitor.visit_function_invocation_node(self)


class ASTIdentifierNode(ASTExpressionNode):
    def __init__(self, identifier):
        super().__init__()
        self.name = "ASTIdentifierNode"
        self.identifier = identifier

    def accept(self, visitor):
        visitor.visit_identifier_node(self)


class ASTMultiplicativeOpNode(ASTExpressionNode):
    def __init__(self, left, operator, right):
        super().__init__()
        self.name = "ASTMultiplicativeOpNode"
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        visitor.visit_multiplicative_op_node(self)


class ASTAdditiveOpNode(ASTExpressionNode):
    def __init__(self, left, operator, right):
        super().__init__()
        self.name = "ASTAdditiveOpNode"
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        visitor.visit_additive_op_node(self)


class ASTRelationalOpNode(ASTExpressionNode):
    def __init__(self, left, operator, right):
        super().__init__()
        self.name = "ASTRelationalOpNode"
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        visitor.visit_relational_op_node(self)


class ASTActualParamsNode(ASTExpressionNode):
    def __init__(self, parameters):
        super().__init__()
        self.name = "ASTActualParamsNode"
        self.parameters = parameters  # List of ASTExpressionNode

    def accept(self, visitor):
        visitor.visit_actual_params_node(self)


class ASTUnaryNode(ASTExpressionNode):
    def __init__(self, operator, operand):
        super().__init__()
        self.name = "ASTUnaryNode"
        self.operator = operator
        self.operand = operand

    def accept(self, visitor):
        visitor.visit_unary_node(self)


class ASTSubExpressionNode(ASTExpressionNode):
    def __init__(self, expression):
        super().__init__()
        self.name = "ASTSubExpressionNode"
        self.expression = expression

    def accept(self, visitor):
        visitor.visit_sub_expression_node(self)


class ASTFunctionCallNode(ASTExpressionNode):
    def __init__(self, identifier, actual_params):
        super().__init__()
        self.name = "ASTFunctionCallNode"
        self.identifier = identifier
        self.actual_params = actual_params

    def accept(self, visitor):
        visitor.visit_function_call_node(self)


class ASTVariableDeclarationNode(ASTStatementNode):
    def __init__(self, identifier, type, suffix=None):
        super().__init__()
        self.name = "ASTVariableDeclarationNode"
        self.identifier = identifier
        self.type = type
        self.suffix = suffix

    def accept(self, visitor):
        visitor.visit_variable_declaration_node(self)


class ASTIfStatementNode(ASTStatementNode):
    def __init__(self, condition, true_block, false_block=None):
        super().__init__()
        self.name = "ASTIfStatementNode"
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def accept(self, visitor):
        visitor.visit_if_statement_node(self)


class ASTWhileStatementNode(ASTStatementNode):
    def __init__(self, condition, block):
        super().__init__()
        self.name = "ASTWhileStatementNode"
        self.condition = condition
        self.block = block

    def accept(self, visitor):
        visitor.visit_while_statement_node(self)


class ASTForStatementNode(ASTStatementNode):
    def __init__(self, initialization, condition, increment, block):
        super().__init__()
        self.name = "ASTForStatementNode"
        self.initialization = initialization
        self.condition = condition
        self.increment = increment
        self.block = block

    def accept(self, visitor):
        visitor.visit_for_statement_node(self)


class ASTReturnStatementNode(ASTStatementNode):
    def __init__(self, expression):
        super().__init__()
        self.name = "ASTReturnStatementNode"
        self.expression = expression

    def accept(self, visitor):
        visitor.visit_return_statement_node(self)


class ASTPrintStatementNode(ASTStatementNode):
    def __init__(self, expression):
        super().__init__()
        self.name = "ASTPrintStatementNode"
        self.expression = expression

    def accept(self, visitor):
        visitor.visit_print_statement_node(self)


class ASTFormalParamNode(ASTNode):
    def __init__(self, identifier, type, size=None):
        super().__init__()
        self.name = "ASTFormalParamNode"
        self.identifier = identifier
        self.type = type
        self.size = size  # Optional size for array types, etc.

    def accept(self, visitor):
        visitor.visit_formal_param_node(self)


class ASTFormalParamsNode(ASTNode):
    def __init__(self, params):
        super().__init__()
        self.name = "ASTFormalParamsNode"
        self.params = params  # List of ASTFormalParamNode

    def accept(self, visitor):
        visitor.visit_formal_params_node(self)


class ASTFunctionDecNode(ASTNode):
    def __init__(self, identifier, formal_params, return_type, block):
        super().__init__()
        self.name = "ASTFunctionDecNode"
        self.identifier = identifier
        self.formal_params = formal_params
        self.return_type = return_type
        self.block = block

    def accept(self, visitor):
        visitor.visit_function_dec_node(self)


class ASTProgramNode(ASTNode):
    def __init__(self, blocks):
        super().__init__()
        self.name = "ASTProgramNode"
        self.blocks = blocks

    def accept(self, visitor):
        visitor.visit_program_node(self)


class ASTVisitor:

    def visit_boolean_literal_node(self, node):
        raise NotImplementedError()

    def visit_float_literal_node(self, node):
        raise NotImplementedError()

    def visit_type_node(self, node):
        raise NotImplementedError()

    def visit_integer_node(self, node):
        raise NotImplementedError()

    def visit_assignment_node(self, node):
        raise NotImplementedError()

    def visit_variable_node(self, node):
        raise NotImplementedError()

    def visit_block_node(self, node):
        raise NotImplementedError()

    def visit_colour_literal_node(self, node):
        raise NotImplementedError()

    def visit_function_invocation_node(self, node):
        raise NotImplementedError()

    def visit_identifier_node(self, node):
        raise NotImplementedError()

    def visit_multiplicative_op_node(self, node):
        raise NotImplementedError()

    def visit_additive_op_node(self, node):
        raise NotImplementedError()

    def visit_relational_op_node(self, node):
        raise NotImplementedError()

    def visit_actual_params_node(self, node):
        raise NotImplementedError()

    def visit_unary_node(self, node):
        raise NotImplementedError()

    def visit_sub_expression_node(self, node):
        raise NotImplementedError()

    def visit_function_call_node(self, node):
        raise NotImplementedError()

    def visit_variable_declaration_node(self, node):
        raise NotImplementedError()

    def visit_if_statement_node(self, node):
        raise NotImplementedError()

    def visit_while_statement_node(self, node):
        raise NotImplementedError()

    def visit_return_statement_node(self, node):
        raise NotImplementedError()

    def visit_print_statement_node(self, node):
        raise NotImplementedError()

    def visit_formal_param_node(self, node):
        raise NotImplementedError()

    def visit_formal_params_node(self, node):
        raise NotImplementedError()

    def visit_function_dec_node(self, node):
        raise NotImplementedError()

    def visit_program_node(self, node):
        raise NotImplementedError()

    def inc_tab_count(self):
        raise NotImplementedError()

    def dec_tab_count(self):
        raise NotImplementedError()


class PrintNodesVisitor(ASTVisitor):
    def __init__(self):
        self.name = "Print Tree Visitor"
        self.node_count = 0
        self.tab_count = 0

    def visit_boolean_literal_node(self, bool_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Boolean Literal::", bool_node.value)

    def visit_float_literal_node(self, float_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Float Literal::", float_node.value)

    def visit_type_node(self, type_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Type::", type_node.type_name)

    def inc_tab_count(self):
        self.tab_count += 1

    def dec_tab_count(self):
        self.tab_count -= 1

    def visit_integer_node(self, int_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Integer value::", int_node.value)

    def visit_assignment_node(self, ass_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Assignment node => ")
        self.inc_tab_count()
        ass_node.id.accept(self)
        ass_node.expr.accept(self)
        self.dec_tab_count()

    def visit_variable_node(self, var_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Variable => ", var_node.lexeme)

    def visit_block_node(self, block_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Block Start:")
        self.inc_tab_count()
        for stmt in block_node.statements:
            stmt.accept(self)
        self.dec_tab_count()
        print('\t' * self.tab_count, "Block End")


    def visit_colour_literal_node(self, colour_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Colour Literal::", colour_node.value)

    def visit_function_invocation_node(self, function_node):
        self.node_count += 1
        print('\t' * self.tab_count, f"Function Invocation::{function_node.function_name} with args:")
        self.inc_tab_count()
        for arg in function_node.arguments:
            arg.accept(self)
        self.dec_tab_count()

    def visit_identifier_node(self, identifier_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Identifier::", identifier_node.identifier)

    def visit_multiplicative_op_node(self, op_node):
        self.node_count += 1
        print('\t' * self.tab_count, f"Multiplicative Operation ({op_node.operator}) between:")
        self.inc_tab_count()
        op_node.left.accept(self)
        op_node.right.accept(self)
        self.dec_tab_count()

    def visit_additive_op_node(self, op_node):
        self.node_count += 1
        print('\t' * self.tab_count, f"Additive Operation ({op_node.operator}) between:")
        self.inc_tab_count()
        op_node.left.accept(self)
        op_node.right.accept(self)
        self.dec_tab_count()

    def visit_relational_op_node(self, op_node):
        self.node_count += 1
        print('\t' * self.tab_count, f"Relational Operation ({op_node.operator}) between:")
        self.inc_tab_count()
        op_node.left.accept(self)
        op_node.right.accept(self)
        self.dec_tab_count()

    def visit_actual_params_node(self, params_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Actual Parameters:")
        self.inc_tab_count()
        for param in params_node.parameters:
            param.accept(self)
        self.dec_tab_count()

    def visit_unary_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, f"Unary Operation: {node.operator} {node.operand.name}")

    def visit_sub_expression_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "SubExpression:")
        self.inc_tab_count()
        node.expression.accept(self)
        self.dec_tab_count()

    def visit_function_call_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, f"Function Call: {node.identifier} with params:")
        self.inc_tab_count()
        for param in node.actual_params:
            param.accept(self)
        self.dec_tab_count()

    def visit_variable_declaration_node(self, node):
        self.node_count += 1
        suffix = f" {node.suffix}" if node.suffix else ""
        print('\t' * self.tab_count, f"Variable Declaration: {node.identifier} as {node.type}{suffix}")

    def visit_if_statement_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "If Statement:")
        self.inc_tab_count()
        print('\t' * self.tab_count, "Condition:")
        node.condition.accept(self)
        print('\t' * self.tab_count, "True Block:")
        node.true_block.accept(self)
        if node.false_block:
            print('\t' * self.tab_count, "Else Block:")
            node.false_block.accept(self)
        self.dec_tab_count()

    def visit_while_statement_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "While Loop:")
        self.inc_tab_count()
        print('\t' * self.tab_count, "Condition:")
        node.condition.accept(self)
        print('\t' * self.tab_count, "Loop Block:")
        node.block.accept(self)
        self.dec_tab_count()

    def visit_for_statement_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "For Loop:")
        self.inc_tab_count()
        print('\t' * self.tab_count, "Initialization:")
        node.initialization.accept(self)
        print('\t' * self.tab_count, "Condition:")
        node.condition.accept(self)
        print('\t' * self.tab_count, "Increment:")
        node.increment.accept(self)
        print('\t' * self.tab_count, "Loop Block:")
        node.block.accept(self)
        self.dec_tab_count()

    def visit_return_statement_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "Return Statement:")
        self.inc_tab_count()
        node.expression.accept(self)
        self.dec_tab_count()

    def visit_print_statement_node(self, node):
        self.node_count += 1
        print('\t' * self.tab_count, "Print Statement:")
        self.inc_tab_count()
        node.expression.accept(self)
        self.dec_tab_count()

    def visit_formal_param_node(self, param_node):
        self.node_count += 1
        size_display = f" of size {param_node.size}" if param_node.size else ""
        print('\t' * self.tab_count, f"Formal Param:: {param_node.identifier} of type {param_node.type}{size_display}")

    def visit_formal_params_node(self, params_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Formal Parameters:")
        self.inc_tab_count()
        for param in params_node.params:
            param.accept(self)
        self.dec_tab_count()

    def visit_function_dec_node(self, function_node):
        self.node_count += 1
        print('\t' * self.tab_count, f"Function Declaration:: {function_node.identifier}")
        self.inc_tab_count()
        function_node.formal_params.accept(self)
        print('\t' * self.tab_count, f"Returns:: {function_node.return_type}")
        function_node.block.accept(self)
        self.dec_tab_count()

    def visit_program_node(self, program_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Program Start:")
        self.inc_tab_count()
        for block in program_node.blocks:
            block.accept(self)
        self.dec_tab_count()
        print('\t' * self.tab_count, "Program End")



# Create a print visitor instance
print_visitor = PrintNodesVisitor()

# assume root node the AST assignment node ....
# x=23
print("Building AST for assigment statement x=23;")
assignment_lhs = ASTVariableNode("x")
assignment_rhs = ASTIntegerNode(23)
root = ASTAssignmentNode(assignment_lhs, assignment_rhs)
root.accept(print_visitor)
print("Node Count => ", print_visitor.node_count)
print("----")
# assume root node the AST variable node ....
# x123
print("Building AST for variable x123;")
root = ASTVariableNode("x123")
root.accept(print_visitor)
print("Node Count => ", print_visitor.node_count)
