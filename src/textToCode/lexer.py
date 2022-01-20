import re

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
    # Integer or floating point number
    "NUM": [r"\d+(?:\.\d+)?"],
    # End of line
    "EOL": [r"\.( |$)", r"then"],
    # Unary negative operator
    "UOP_NEG": [r"negative"],
    # Modifiable block statment (ex: if ...:)
    "KWD_BLK_MOD": ["if", "else if", "while", "for", "catch"],
    # Unmodifiable block statment (ex: else:)
    "KWD_BLK_NMD": ["else", "try", "finally"],
    # Symbols with one to one corrispondence
    "SYM": ["in", "and", "or", "(is )?set to", "none", "true", "false"],
    # Comparison operators
    "CMP": [r"(is )?equal to", r"(is )?not equal to", r"(is )?greater than or equal to",
            r"(is )?less than or equal to", r"(is )?less than", r"(is )?greater than"],
    # End of block
    "END": ["end"],
    # Open string
    "STR_OPN": ["(single )?quote"],
    # Close string
    "STR_CLS": ["un(single )?quote"],
    # Set variable
    "VAR_SET": ["set"],
    # Escape symbol
    "ESC": ["real"],
    
    # Identifier
    "ID": [r"[a-z]+"],
  }
  
  def __init__(self):
    # Pattern matching string for tokens
    self.TKN_MATCH = "|".join([f"(?P<{t}>{'|'.join([f'(?:{a})' for a in self.TOKENS[t]])})" for t in self.TOKENS])
  
  def lex(self, code: str):
    """Converts text string into labled tokens

    Args:
        code (str): Code to lex

    Returns:
        list[Token]: Output tokens
    """    
    matches = re.finditer(self.TKN_MATCH, code.lower())
    lineno = 0
    linestart = 0
    tokens = []
    
    for match in matches:
      
      tkn = Token(match.lastgroup, match.group(0), lineno, match.start() - linestart)
      
      # Track line/column number
      if tkn.type == "EOL":
        lineno += 1
        linestart = match.end()
      tokens.append(tkn)
      
    return tokens
