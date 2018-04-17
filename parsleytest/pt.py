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
	
def makefn(name, input, output, body):
	res = 'struct ' + name + '_result{'
	for par in output:
		res += par['decl'] + '; '
	res += '}\n'
	res += name + '_result ' + name + '('
	for par in input:
		res += par['decl']
		if par['asgn'] != None:
			res += '=' + par['asgn']
		res += ', '
	res += '){\n'
	for par in output:
		res += '\t' + par['decl']
		if par['asgn'] != None:
			res += '=' + par['asgn']
		res += ';\n'	
	res += '#define Return return {' # ugly hack until I todo this properly
	for par in output:
		res += par['id'] + ', '
	res += '};\n\n'
	
	res += body + '\n\n'
	res += '\tReturn\n#undef Return'
	res += '}\n'
	
	return res
	
fiascode = parsley.makeGrammar("""

code = (known | anything)*:c -> ''.join(c)


known = (comment | string | substitution | group | stray)
stray = (groupstray | ifstray):estray -> exception('Stray ' + estray + ' detected')

comment = (comment1 | comment2)
comment1 = <'/*' (~'*/' anything)* '*/'>
comment2 = <'//' (~'\n' anything)* '\n'>

ws = (' ' | '\\t' | '\\r' | '\\n' | comment)*

string = <'"' (escaped | ~'"' anything)* '"'>
escaped = <'\\\\' anything> # we need a double backslash escape here for representing one backslash

group = (parenthesed | bracketed | braced)
parenthesed = '(' (~')' (known | anything))*:body ')' -> '(' + ''.join(body) + ')'
bracketed   = '[' (~']' (known | anything))*:body ']' -> '[' + ''.join(body) + ']'
braced      = '{' (~'}' (known | anything))*:body '}' -> '{' + ''.join(body) + '}'
groupstray = (')' | ']' | '}')

identifier = <(letter | '_') (letter | '_' | digit)*>


substitution = ifstmt | forstmt | function # actual fiascode 


ifstmt     = 'If'     condition:cond 'Then'   ifbody:body (elseifstmt | elsestmt | endifstmt):tail ->      'if(' + cond + '){' + ''.join(body) + '}' + tail
elseifstmt = 'Elseif' condition:cond 'Then'   ifbody:body (elseifstmt | elsestmt | endifstmt):tail -> 'else if(' + cond + '){' + ''.join(body) + '}' + tail
elsestmt   = 'Else'                         elsebody:body                          endifstmt :tail -> 'else{'                  + ''.join(body) + '}' + tail
endifstmt  = 'Endif' -> ''

condition = (~'Then' (known | anything))*:cond -> ''.join(cond)
ifbody    = (~('Elseif' | 'Else' | 'Endif') (known | anything))*:body -> ''.join(body)
elsebody  = (~'Endif' (known | anything))*:body -> ''.join(body)

ifstray = ('Elseif' | 'Else' | 'Endif' | 'Then') # those should not be encountered first


function = 'Fn' ws identifier:name ws '(' parameterlist:input ')' ws '->' ws '(' parameterlist:output ')' fnbody:body 'Endfn'-> makefn(name, input, output, body)
parameterlist = parameter:first (',' parameter)*:rest -> [first] + rest if first!=[] else []
parameter = ws (~(')' | ',' | '=')(known | identifier:id | anything))*:decl ('=' assignment)?:asgn -> {'decl':''.join(decl), 'id':id, 'asgn':asgn} if decl != [] else []
assignment = (~(')' | ',')(known | anything))*:asgn -> ''.join(asgn)
fnbody  = (~'Endfn' (known | anything))*:body -> ''.join(body)

forstmt = 'For' 

""", {'exception':exception, 'makefn':makefn})

    #for(int x=0, y=0, w=3, h=3; y<h; x++, y+=x>=w?1:0, x=x>=w?0:x){
   #     std::cout << x << y << "\n";
  #  }

print(fiascode("""Fn a(&a, int b,   c=3)->(uint d,e=4,f) bibabu Endfn""").function())
#print(fiascode("""Fn u()->()""").function())



