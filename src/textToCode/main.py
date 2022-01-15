import lexer
import transpiler


if __name__ == "__main__":
  code = "set a variable to Negative 100. If a variable is equal to 100. another cool variable is set to 10. else if a variable is greater than 2 and a variable is less than 5. j is set to Negative 5.23. end. h is set to 7.87. quote quote single quote unsingle quote unquote unquote then 5."
  lex = lexer.Lexer()
  trans = transpiler.Transpiler()
  for i in lex.lex(code):
    print(i)
  result = trans.transpile(lex.lex(code))
  print("--- PYTHON START ---")
  print(result)
  print("--- OUTPUT START ---")
  exec(result)
