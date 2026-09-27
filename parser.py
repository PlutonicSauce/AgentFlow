from ast_nodes import *

class ParserError(Exception):
    def __init__(self, message, line, col, code_str):
        lines = code_str.split('\n')
        err_line = lines[line - 1] if line <= len(lines) else ""
        pointer = " " * (col - 1) + "^"
        super().__init__(f"{message}\n  {err_line}\n  {pointer}")

class Parser:
    def __init__(self, tokens, code_str):
        self.tokens = tokens
        self.code_str = code_str
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def error(self, msg, tok=None):
        if not tok: tok = self.current()
        raise ParserError(f"Parse Error at line {tok.line}, col {tok.col}: {msg}", tok.line, tok.col, self.code_str)

    def consume(self, expected_type=None, expected_value=None):
        tok = self.current()
        if expected_type and tok.type != expected_type:
            self.error(f"Expected type {expected_type}, got {tok.type}", tok)
        if expected_value and tok.value != expected_value:
            self.error(f"Expected value '{expected_value}', got '{tok.value}'", tok)
        self.pos += 1
        return tok

    def match(self, expected_type=None, expected_value=None):
        tok = self.current()
        if expected_type and tok.type != expected_type: return False
        if expected_value and tok.value != expected_value: return False
        return True

    def parse(self):
        statements = []
        while not self.match("EOF"):
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        if self.match("KEYWORD", "agent"):
            return self.parse_agent_decl()
        elif self.match("KEYWORD", "flow"):
            return self.parse_flow_decl()
        elif self.match("KEYWORD", "run"):
            return self.parse_run_stmt()
        else:
            self.error("Unexpected top-level statement")

    def parse_agent_decl(self):
        self.consume("KEYWORD", "agent")
        name = self.consume("IDENT").value
        self.consume("{")
        props = {}
        while not self.match("}"):
            prop_name = self.consume("IDENT").value
            self.consume(":")
            props[prop_name] = self.parse_expression()
        self.consume("}")
        return AgentDecl(name, props)

    def parse_flow_decl(self):
        self.consume("KEYWORD", "flow")
        name = self.consume("IDENT").value
        self.consume("(")
        params = []
        if not self.match(")"):
            params.append(self.consume("IDENT").value)
            while self.match(","):
                self.consume(",")
                params.append(self.consume("IDENT").value)
        self.consume(")")
        
        self.consume("{")
        body = []
        while not self.match("}"):
            body.append(self.parse_flow_stmt())
        self.consume("}")
        return FlowDecl(name, params, body)

    def parse_flow_stmt(self):
        if self.match("KEYWORD", "return"):
            self.consume("KEYWORD", "return")
            return ReturnStmt(self.parse_expression())
            
        if self.match("IDENT") and self.tokens[self.pos+1].value == "=":
            target = self.consume("IDENT").value
            self.consume("=")
            return Assignment(target, self.parse_expression())
            
        return self.parse_expression()

    def parse_run_stmt(self):
        self.consume("KEYWORD", "run")
        name = self.consume("IDENT").value
        self.consume("(")
        args = []
        if not self.match(")"):
            args.append(self.parse_expression())
            while self.match(","):
                self.consume(",")
                args.append(self.parse_expression())
        self.consume(")")
        return RunStmt(name, args)

    def parse_expression(self):
        tok = self.current()
        if tok.type == "STRING":
            self.consume("STRING")
            return StringLiteral(tok.value)
        elif tok.type == "NUMBER":
            self.consume("NUMBER")
            return NumberLiteral(tok.value)
        elif tok.value == "[":
            self.consume("[")
            elements = []
            if not self.match("]"):
                elements.append(self.parse_expression())
                while self.match(","):
                    self.consume(",")
                    elements.append(self.parse_expression())
            self.consume("]")
            return ListLiteral(elements)
        elif tok.type == "KEYWORD" and tok.value == "retry":
            self.consume("KEYWORD", "retry")
            count = self.consume("NUMBER").value
            self.consume("{")
            body = []
            while not self.match("}"):
                body.append(self.parse_flow_stmt())
            self.consume("}")
            return RetryStmt(count, body)
        elif tok.type == "IDENT":
            if self.tokens[self.pos+1].value == ".":
                obj = self.consume("IDENT").value
                self.consume(".")
                method_tok = self.current()
                if method_tok.type == "IDENT" or (method_tok.type == "KEYWORD" and method_tok.value == "run"):
                    method = method_tok.value
                    self.consume()
                else:
                    self.error(f"Expected method name, got {method_tok.type}", method_tok)
                self.consume("(")
                args = []
                if not self.match(")"):
                    args.append(self.parse_expression())
                    while self.match(","):
                        self.consume(",")
                        args.append(self.parse_expression())
                self.consume(")")
                return MethodCall(obj, method, args)
            else:
                return Identifier(self.consume("IDENT").value)
        
        self.error("Unexpected expression")
