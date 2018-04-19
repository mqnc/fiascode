import sys
import os
cd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cd + "/parsley")
import parsley # rename parsley/parsley.py to parsley/__init__.py

if 0:
	grammar = parsley.makeGrammar("""
		test= ('::' | ~':' anything)*:a anything*:b -> ''.join(a) + '!' + ''.join(b)
	""", {})

	print(grammar("abc::de:efg::hi").test())


def exception(txt):
	raise SyntaxError(txt)
	return txt


def makefor(iters, body):

	res = '{\n'
	res += 'bool break_nesting = false;\n'

	for ig in iters: # iterate through groups
		for it in ig: # iterate through iterators in group
			var = it['id']
			iter = var + '__iterator';
			if it['type'] == '=':
				range = var + '__range'
				res += 'const auto ' + range + ' = ' + it['asgn'] + ';\n'
			elif it['type'] == ':':
				range = it['asgn']
			it['range'] = range
			res += 'auto *' + iter + ' = begin(' + range + ');\n';
			
		res += 'for(; '
		for it in ig: # iterate through iterators in group
			res += it['id'] + '__iterator != end(' + it['range'] + ') && '
		res = res[:-4] # delete last " && "
		res += "; "
		for it in ig: # iterate through iterators in group
			res += it['id'] + '__iterator++, '
		res = res[:-2] # delete last ", "
		res += '){\n'
		for it in ig: # iterate through iterators in group
			res += '\t auto &' + it['id'] + ' = *' + it['id'] + '__iterator;\n'
			
	res += '#define Break break_nesting = true; break;\n\n'
	res += body
	res += '\n\n#undef Break\n'
	
	for ig in iters: # iterate through groups
		res += 'if(break_nesting){break;}\n}\n'
	
	res += '\n}\n'
	return res
	
	
def makefn(name, input, output, body):

	res = ''
	
	if isinstance(output, str): # output is a string, not a list -> no struct for return
		res = output + ' ' + name + '('
		for par in input:
			res += par['decl']
			if par['asgn'] != None: res += '=' + par['asgn']
			res += ', '
		if len(input) != 0: res = res[:-2]; # delete last comma
		res += '){\n\n'
		res += body + '\n\n}\n'
	
	else:
		res = 'struct ' + name + '__result{'
		for par in output:
			res += par['decl'] + '; '
		res += '};\n'
		res += name + '__result ' + name + '('
		for par in input:
			res += par['decl']
			if par['asgn'] != None: res += '=' + par['asgn']
			res += ', '
		if len(input) != 0: res = res[:-2]; # delete last comma
		res += '){\n'
		for par in output:
			res += '\t' + par['decl']
			if par['asgn'] != None: res += '=' + par['asgn']
			res += ';\n'
		
		if body != '':
		
			res += '#define Return return {' # ugly hack until I todo this properly
			for par in output:
				res += par['id'] + ', '
			if len(output) != 0: res = res[:-2]; # delete last comma
			res += '};\n'
			
			res += body + '\n'
			res += '\tReturn\n#undef Return\n'
		
		else:
			res += '\treturn {'
			for par in output:
				res += par['id'] + ', '
			if len(output) != 0: res = res[:-2]; # delete last comma
			res += '};\n'
			
		res += '}\n'
	
	return res

'''
{
const auto va__range = va;
auto *a__iterator = begin(va__range);

for(; a__iterator != end(va__range); a__iterator++){
	auto &a = *a__iterator;
	
	
	const auto vb__range = vb;
	auto *b__iterator = begin(vb__range);
	const auto vc__range = std::vc;
	auto *c__iterator = begin(vb__range);	
	
	for(; b__iterator != end(vb__range) && c__iterator != end(vc__range); b__iterator++, c__iterator++){
	
		...
		
		
		
a:va, [int b:vb, std::c:std::vc], d:1..2, e:{1,2,3,4}	
'''	

	
fiascode = parsley.makeGrammar("""

code = symbol*:c -> ''.join(c)

symbol = knownsymbol | identifier | anything
knownsymbol = (comment | string | substitution | group | stray)
stray = (groupstray | ifstray | fnstray | loopstray | switchstray):estray -> exception('Stray ' + estray + ' detected')

comment = (comment1 | comment2)
comment1 = <'/*' (~'*/' anything)* '*/'>
comment2 = <'//' (~'\n' anything)* '\n'>

ws = (' ' | '\\t' | '\\r' | '\\n' | comment)*

string = <'"' (escaped | ~'"' anything)* '"'>
escaped = <'\\\\' anything> # represents one backslash (double escape needed)

group = (parenthesed | bracketed | braced)
parenthesed = '(' (~')' symbol)*:body ')' -> '(' + ''.join(body) + ')'
bracketed   = '[' (~']' symbol)*:body ']' -> '[' + ''.join(body) + ']'
braced      = '{' (~'}' symbol)*:body '}' -> '{' + ''.join(body) + '}'
groupstray = (')' | ']' | '}')

identifier = <(letter | '_') (letter | '_' | digit)*>


substitution = branchstmt | loopstmt | functionstmt # actual fiascode 


branchstmt = ifstmt | switchstmt

ifstmt     = 'If'     ifcondition:cond 'Then'   ifbody:body (elseifstmt | elsestmt | endifstmt):tail ->      'if(' + cond + '){' + ''.join(body) + '}' + tail
elseifstmt = 'Elseif' ifcondition:cond 'Then'   ifbody:body (elseifstmt | elsestmt | endifstmt):tail -> 'else if(' + cond + '){' + ''.join(body) + '}' + tail
elsestmt   = 'Else'                         elsebody:body                          endifstmt :tail -> 'else{'                  + ''.join(body) + '}' + tail
endifstmt  = 'Endif' -> ''
ifcondition = (~'Then' symbol)*:cond -> ''.join(cond)
ifbody    = (~('Elseif' | 'Else' | 'Endif') symbol)*:body -> ''.join(body)
elsebody  = (~'Endif' symbol)*:body -> ''.join(body)
ifstray = ('Elseif' | 'Else' | 'Endif' | 'Then') # those should not be encountered first

switchstmt = 'Switch' switchcondition:cond switchbody:body 'Endswitch' -> 'switch(' + cond + '){\\n' + body + '\\n}'
switchcondition = (~'Case' symbol)*:cond -> ''.join(cond)
switchbody = (case | default)+:body -> ''.join(body)
case = 'Case' casecondition:cond 'Do' casebody:body caseend:end -> 'case ' + cond + ':\\n\\t' + body + '\\n' + end
default = 'Default' casebody:body -> '\\n' 'default: ' + body
casecondition = (~'Do' symbol)*:cond -> ''.join(cond)
casebody = (~('Case' | 'Fall' | 'Default' | 'Endswitch')symbol)*:body -> ''.join(body)
caseend = ('Fall' ws -> '') | (ws -> 'break;')
switchstray = ('Case' | 'Default' | 'Fall' | 'Endswitch' | 'Do')


loopstmt = forstmt | whilestmt | repeatstmt

forstmt = 'For' iteratorlist:iters 'Do' forbody:body 'Loop' -> makefor(iters, body)
iteratorlist = ws iteratoritem:first ws (',' ws iteratoritem)*:rest -> [first] + rest
iteratoritem = (iteratorgroup:iter -> iter) | (iterator:iter -> [iter])
iteratorgroup = '[' iterator:first (',' ws iterator)*:rest ']' -> [first] + rest
iterator = iterdeclaration:iter (':' | '='):type iterassignment:asgn -> {'decl':iter['decl'], 'id':iter['id'], 'type':type, 'asgn':asgn}
iterdeclaration = ('::' | ~(':' | '=') (knownsymbol | identifier:id | anything))*:decl -> {'decl':''.join(decl), 'id':id}
iterassignment = (~(',' | 'Do' | ']')symbol)*:asgn -> ''.join(asgn)
forbody = (~'Loop' symbol)*:body -> ''.join(body)

whilestmt = 'While' (~'Do' symbol)*:cond 'Do' (~'Loop' symbol)*:body 'Loop' -> 'while(' + ''.join(cond) + '){\\n' + ''.join(body) + '}'
repeatstmt = 'Repeat' (~('Until' | 'Whilst')symbol)*:body (untilcond | whilstcond):cond 'Loop' -> 'do{\\n' + ''.join(body) + '\\n}while(' + cond + ');'
untilcond = 'Until' (~('Loop')symbol)*:cond -> '!(' + ''.join(cond) + ')'
whilstcond = 'Whilst' (~('Loop')symbol)*:cond -> ''.join(cond)
loopstray = ('Do' | 'Until' | 'Whilst' | 'Loop')


functionstmt = 'Fn' ws identifier:name ws inputpars:input ws outputpars:output ws fnbody:body 'Endfn'-> makefn(name, input, output, body)
inputpars = ('(' parameterlist:input ')' | ws:input) -> input
outputpars = ('->' ws '(' parameterlist:output ')' -> output) | ('->' ws returntype:output -> ''.join(output)) | (ws -> 'void')
parameterlist = parameter:first (',' parameter)*:rest -> [first] + rest if first!=[] else []
parameter = ws (~(')' | ',' | '=')(knownsymbol | identifier:id | anything))*:decl ('=' parassignment)?:asgn -> {'decl':''.join(decl), 'id':id, 'asgn':asgn} if decl != [] else []
returntype = ws (~(':=' | 'Endfn')symbol)*:type -> type
parassignment = (~(')' | ',')symbol)*:asgn -> ''.join(asgn)
fnbody = (':=' (~'Endfn' symbol)*:body -> ''.join(body)) | (ws -> '')
fnstray = ('->' | ':=' | 'Endfn')
#todo: virtual inline static bla

""", {'exception':exception, 'makefor':makefor, 'makefn':makefn})


'''
For a:va, [int b:vb, c:vc], d:1..2 Do

Loop
'''




    #for(int x=0, y=0, w=3, h=3; y<h; x++, y+=x>=w?1:0, x=x>=w?0:x){
   #     std::cout << x << y << "\n";
  #  }
'''
print(fiascode("""Fn f1(&a, int b,   c=3)->(uint d,e=4,f):= bibabu Endfn""").function())
print(fiascode("""Fn f2(int x)->(int y):= Endfn""").function())
print(fiascode("""Fn f3()->():= Endfn""").function())
print(fiascode("""Fn f4():= Endfn""").function())
print(fiascode("""Fn f5 ->():= Endfn""").function())
print(fiascode("""Fn f6:= Endfn""").function())
print(fiascode("""Fn f7 -> int := Endfn""").function())
print(fiascode("""Fn div(int x, int y)->(int q=0, int r=0):= q=x/y; r=x%y; Endfn""").function())
print(fiascode("""Fn f9(int x, int y)->(int q=x/y, int r=x%y) Endfn""").function())
print(fiascode("""Switch a Case 3 Do x=3; Fall Case 4 Do x=4; Default x=5 Endswitch""").code())
print(fiascode("""While x<4 Do something Loop""").code())
print(fiascode("""Repeat something Until x<54 Loop""").code())
print(fiascode("""Repeat something Whilst x>=54 Loop""").code())
'''

print(fiascode("""For a=va, [int b=vb, std::c:std::vc], d:1..2, e={1,2,3,4} Do body Loop""").code())

print(fiascode("""For a:va, b:vb, c:vc Do body Loop""").code())




