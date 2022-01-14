import re
from functools import wraps

class Token:
  def __init__(self, type: str, value: str, line: int, col: int):
    self.type = type
    self.value = value
    self.line = line
    self.col = col
    
  def __str__(self):
    return f"('{self.value}': {self.type} @ line {self.line + 1}, col {self.col + 1})"
  
  def __repr__(self):
    return f"({self.type} '{self.value}')"

class Lexer:
  
  TOKENS = {
    "NUM": [r"\d+(?:\.\d+)?"],
    "EOL": [r"\.( |$)", r"then"],
    "UOP_NEG": [r"negative"],
    "KWD_BLK_MOD": ["if", "else if", "while", "for", "catch"],
    "KWD_BLK_NMD": ["else", "try", "finally"],
    "KWD_VAL": ["none", "true", "false"],
    "BOP": ["in", "and", "or", "(is )?set to"],
    "CMP": [r"(is )?equal to", r"(is )?not equal to", r"(is )?greater than or equal to",
            r"(is )?less than or equal to", r"(is )?less than", r"(is )?greater than"],
    "END": ["end"],
    "STR_OPN": ["(single )?quote"],
    "STR_CLS": ["un(single )?quote"],
    "VAR_SET": ["set"],
    
    
    "ID": [r"[a-z]+"],
  }
  
  def __init__(self, code: str):
    self.code = code
    self.token_funcs = {
      
    }
    
    self.TKN_MATCH = "|".join([f"(?P<{t}>{'|'.join([f'(?:{a})' for a in self.TOKENS[t]])})" for t in self.TOKENS])
    
  def lex(self):
    matches = re.finditer(self.TKN_MATCH, self.code.lower())
    lineno = 0
    linestart = 0
    tokens = []
    
    for match in matches:
      tkn = Token(match.lastgroup, match.group(0), lineno, match.start() - linestart)
      if tkn.type in self.token_funcs:
        self.token_funcs[tkn.type](tkn)
      
      if tkn.type == "EOL":
        lineno += 1
        linestart = match.end()
      tokens.append(tkn)
      
    return tokens
