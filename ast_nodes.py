class Node: pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

class AgentDecl(Node):
    def __init__(self, name, props):
        self.name = name
        self.props = props

class FlowDecl(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class RunStmt(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Assignment(Node):
    def __init__(self, target, value):
        self.target = target
        self.value = value

class ReturnStmt(Node):
    def __init__(self, value):
        self.value = value

class RetryStmt(Node):
    def __init__(self, count, body):
        self.count = count
        self.body = body

class MethodCall(Node):
    def __init__(self, obj, method, args):
        self.obj = obj
        self.method = method
        self.args = args

class StringLiteral(Node):
    def __init__(self, value):
        self.value = value

class NumberLiteral(Node):
    def __init__(self, value):
        self.value = value

class ListLiteral(Node):
    def __init__(self, elements):
        self.elements = elements

class Identifier(Node):
    def __init__(self, name):
        self.name = name
