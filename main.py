import sys
from lexer import lex
from parser import Parser, ParserError
from interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.af>")
        sys.exit(1)
        
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        code = f.read()
        
    try:
        tokens = lex(code)
        parser = Parser(tokens, code)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
    except ParserError as e:
        print(f"\n[AgentFlow] {e}")
    except Exception as e:
        print(f"\n[AgentFlow] Execution Error: {e}")

if __name__ == "__main__":
    main()
