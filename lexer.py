class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line}, col={self.col})"

KEYWORDS = {"agent", "flow", "run", "return", "retry"}

def lex(code):
    tokens = []
    line_num = 1
    col_num = 1
    i = 0
    while i < len(code):
        char = code[i]
        
        # Comments
        if char == '/' and i + 1 < len(code) and code[i+1] == '/':
            while i < len(code) and code[i] != '\n':
                i += 1
                col_num += 1
            continue

        if char.isspace():
            if char == '\n':
                line_num += 1
                col_num = 1
            else:
                col_num += 1
            i += 1
            continue
            
        if char in "{}():=[],.":
            tokens.append(Token(char, char, line_num, col_num))
            i += 1
            col_num += 1
            continue
            
        if char == '"':
            start_col = col_num
            i += 1
            col_num += 1
            start = i
            while i < len(code) and code[i] != '"':
                if code[i] == '\n': 
                    line_num += 1
                    col_num = 1
                else:
                    col_num += 1
                i += 1
            tokens.append(Token("STRING", code[start:i], line_num, start_col))
            i += 1
            col_num += 1
            continue
            
        if char.isdigit():
            start_col = col_num
            start = i
            while i < len(code) and code[i].isdigit():
                i += 1
                col_num += 1
            tokens.append(Token("NUMBER", int(code[start:i]), line_num, start_col))
            continue
        
        if char.isalpha() or char == '_':
            start_col = col_num
            start = i
            while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                i += 1
                col_num += 1
            val = code[start:i]
            if val in KEYWORDS:
                tokens.append(Token("KEYWORD", val, line_num, start_col))
            else:
                tokens.append(Token("IDENT", val, line_num, start_col))
            continue
            
        raise Exception(f"Lexical Error at line {line_num}, col {col_num}: Unexpected character '{char}'")
        
    tokens.append(Token("EOF", "EOF", line_num, col_num))
    return tokens
