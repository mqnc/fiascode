import sys
import os
cd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cd + "/parsley")
import parsley # rename parsley/parsley.py to parsley/__init__.py

if True:
	grammar = parsley.makeGrammar("""
	
	word = <letter+>
	term = '[' (~']' (word:w | anything))*:i ']' -> (''.join(i), w)
	
	test term:t -> 'Term is "' + t[0] + '", last word is "' + t[1] + '"'
	
	
	""", {})

	print(grammar("[ich +bin ein 20-Test]").test())


def exception(txt):
	raise SyntaxError(txt)
	return txt
	
fiascode = parsley.makeGrammar("""

code = (known | anything)*:c -> ''.join(c)


known = (comment | string | substitution | group | stray)
stray = (groupstray | ifstray):estray -> exception('Stray ' + estray + ' detected')

comment = (comment1 | comment2)
comment1 = <'/*' (~'*/' anything)* '*/'>
comment2 = <'//' (~'\n' anything)* '\n'>

string = <'"' (escaped | ~'"' anything)* '"'>
escaped = <'\\\\' anything> # we need a double backslash escape here for representing one backslash

group = (parenthesed | bracketed | braced)
parenthesed = '(' (~')' (known | anything))*:body ')' -> '(' + ''.join(body) + ')'
bracketed   = '[' (~']' (known | anything))*:body ']' -> '[' + ''.join(body) + ']'
braced      = '{' (~'}' (known | anything))*:body '}' -> '{' + ''.join(body) + '}'
groupstray = (')' | ']' | '}')

identifier = <(letter | '_') (letter | '_' | digit)*>


substitution = ifstmt | forstmt # actual fiascode 


ifstmt     = 'If'     condition:cond 'Then'   ifbody:body (elseifstmt | elsestmt | endifstmt):tail ->      'if(' + cond + '){' + ''.join(body) + '}' + tail
elseifstmt = 'Elseif' condition:cond 'Then'   ifbody:body (elseifstmt | elsestmt | endifstmt):tail -> 'else if(' + cond + '){' + ''.join(body) + '}' + tail
elsestmt   = 'Else'                         elsebody:body                          endifstmt :tail -> 'else{'                  + ''.join(body) + '}' + tail
endifstmt  = 'Endif' -> ''

condition = (~'Then' (known | anything))*:cond -> ''.join(cond)
ifbody    = (~('Elseif' | 'Else' | 'Endif') (known | anything))*:body -> ''.join(body)
elsebody  = (~'Endif' (known | anything))*:body -> ''.join(body)

ifstray = ('Elseif' | 'Else' | 'Endif' | 'Then') # those should not be encountered first



forstmt = 'For' 

""", {'exception':exception})

    #for(int x=0, y=0, w=3, h=3; y<h; x++, y+=x>=w?1:0, x=x>=w?0:x){
   #     std::cout << x << y << "\n";
  #  }

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
	Endif
Endif

""").code())



