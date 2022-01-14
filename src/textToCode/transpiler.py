import lexer
import re

class Transpiler:
  def __init__(self, tokens: list[lexer.Token], indent: str="  "):
    self.tokens = tokens
    self.indent = indent
    self.result = ""
    self.indent_level = 0
  
  def emit(self, *s: str, join: str=" ", end: str=" "):
    """Appends s to result

    Args:
        join (str, optional): String to join s with. Defaults to " ".
        end (str, optional): String to add to end of emit. Defaults to " ".
    """
    self.result += join.join(s) + end
  
  # TODO: Pass tokens directly into function instead of object
  def transpile(self):
    """Transpiles list of lexer.Token into Python code string"""
    # If currently in a block start statment
    in_stmt = False
    # If the next token is on a new line
    new_line = True
    # Nesting level of current string
    str_lvl = 0
    
    tknno = 0
    while tknno < len(self.tokens):
      tkn = self.tokens[tknno]
      
      # Auto-unindent
      if tkn.value in ["else if", "else", "catch", "end"]:
        self.indent_level -= 1
      
      # Emit indent
      if new_line:
        self.emit(self.indent * self.indent_level, end="")
        new_line = False
      
      if tkn.type == "KWD_BLK_MOD":
        in_stmt = True
        self.emit(tkn.value if tkn.value != "else if" else "elif")
      elif tkn.type == "KWD_BLK_NMD":
        self.indent_level += 1
        self.emit(tkn.value + ":")
      elif tkn.type == "EOL":
        if in_stmt:
          # End modifiable block statment
          self.indent_level += 1
          self.emit(":", end="")
          in_stmt = False
        self.emit("\n", end='')
        new_line = True
      elif tkn.type == "KWD_VAL":
        # TODO: Merge BOP and KWD_VAL
        self.emit({
          "none": "None",
          "true": "True",
          "false": "False"
        }[tkn.value])
      elif tkn.type in "NUM":
        self.emit(tkn.value)
      elif tkn.type == "UOP_NEG":
        self.emit("-", end="")
      elif tkn.type == "VAR_SET":
        # Convert 'set [var] to' to '[var] set to'
        t = list(filter(lambda a: a.value == "to", self.tokens))[0]
        t.value = "set to"
        t.type = "BOP"
      elif tkn.type == "BOP":
        self.emit({
          "in": "in",
          "or": "or",
          "and": "and",
          "set to": "=",
          "is set to": "=",
        }[tkn.value])
      elif tkn.type == "CMP":
        tkn.value = re.sub(r"(^is )|( than$)|( to$)", "", tkn.value)
        self.emit({
          "equal": "==",
          "not equal": "!=",
          "greater than or equal": ">=",
          "less than or equal": "<=",
          "greater": ">",
          "less": "<",
        }[tkn.value])
      elif tkn.type == "STR_OPN":
        if str_lvl > 0:
          # Escape quote in string
          self.emit("\\", end="")
        str_lvl += 1
        self.emit("'" if "single" in tkn.value else "\"", end="")
      elif tkn.type == "STR_CLS":
        str_lvl -= 1
        if str_lvl > 0:
          # Escape quote in string
          self.emit("\\", end="")
        self.emit("'" if "single" in tkn.value else "\"", end="")
      elif tkn.type == "ID":
        # Join consecutive identifiers into one with '_'
        while self.tokens[tknno + 1].type == "ID":
          tkn.value += "_" + self.tokens.pop(tknno + 1).value
        self.emit(tkn.value)
        
        
      tknno += 1
    return self.result