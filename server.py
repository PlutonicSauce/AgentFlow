import sys
import json
import io
import traceback
from http.server import SimpleHTTPRequestHandler, HTTPServer
from lexer import lex
from parser import Parser, ParserError
from interpreter import Interpreter

class IDEHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/templates/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/api/run':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            code = data.get('code', '')

            # Redirect stdout
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout

            try:
                tokens = lex(code)
                parser = Parser(tokens, code)
                ast = parser.parse()
                
                interpreter = Interpreter()
                interpreter.interpret(ast)
                
            except ParserError as e:
                print(f"[AgentFlow] {e}")
            except Exception as e:
                print(f"[AgentFlow] Execution Error: {e}")
                traceback.print_exc()
            finally:
                sys.stdout = old_stdout

            output = new_stdout.getvalue()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'output': output}).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint not found")

if __name__ == '__main__':
    port = 8080
    server_address = ('', port)
    httpd = HTTPServer(server_address, IDEHandler)
    print(f"AgentFlow Web IDE running on http://localhost:{port}")
    httpd.serve_forever()
