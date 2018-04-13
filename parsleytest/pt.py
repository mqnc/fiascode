import sys
import os
cd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cd + "/parsley")
import parsley # rename parsley/parsley.py to parsley/__init__.py


grammar = parsley.makeGrammar("""
lu = letter | '_'
lud = lu | digit
identifier = lu lud*
function = 'Fn' ws <identifier>:fname ws '(' ws <identifier>:param ws ')' -> {"fname":fname, "param":param}
""", {})
print(grammar("Fn abc(defg)").function())

grammar = parsley.makeGrammar("""
number = digit:n -> 'Number' + n
char = letter:l -> 'Letter' + l
sequence = <(number | letter)*>:s -> s
""", {})
print(grammar("R2D2").sequence())