import sys
import os
cd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cd + "/parsley")
import parsley # rename parsley/parsley.py to parsley/__init__.py

'''
grammar = parsley.makeGrammar("""
test (~('a' | 'b') anything)*:t anything*-> ''.join(t).upper()
""", {})

print(grammar("sfdsabwet").test())

'''

fiascode = parsley.makeGrammar("""

code = (known | anything)*:c -> ''.join(c)

known = (comment | string | substitution)

comment = (comment1 | comment2):c -> 'COMMENT[' + c + ']'
comment1 = <'/*' (~'*/' anything)* '*/'>
comment2 = <'//' (~'\n' anything)* '\n'>

string = <'"' (escaped | ~'"' anything)* '"'>:s -> 'STRING[' + s + ']'
escaped = <'\\\\' anything> # we need a double backslash escape here for representing one backslash

substitution = ifstmt

ifstmt     = 'If'     condition:cond 'Then'   ifbody:body (elseifstmt | elsestmt | endifstmt):tail ->      'if(' + cond + '){' + ''.join(body) + '}' + tail
elseifstmt = 'Elseif' condition:cond 'Then'   ifbody:body (elseifstmt | elsestmt | endifstmt):tail -> 'else if(' + cond + '){' + ''.join(body) + '}' + tail
elsestmt   = 'Else'                         elsebody:body                          endifstmt :tail -> 'else{'                  + ''.join(body) + '}' + tail
endifstmt  = 'Endif' -> ''

condition = (known | ~'Then' anything)*:cond -> ''.join(cond)
ifbody    = (known | ~('Elseif' | 'Else' | 'Endif') anything)*:body -> ''.join(body)
elsebody  = (known | ~('Endif') anything)*:body -> ''.join(body)


#forstmt = 'For' ws block:b1 ws 'Do' ws block:b2 ws 'Loop' -> 'for(' + b1 + '){' + b2 + '}'

""", {})

print(fiascode("""

If a>b Then
	If 1 Then 
		2
	Endif
	b=5

	If u=3 Then
		k=4
	Else
		a=7
	Elseif h=8 Then
		g=3
	Endif
Endif

""").code())



