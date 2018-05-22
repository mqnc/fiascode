#hdr
#include<iostream>
#include<cstdlib>
#include<vector>
#end

using namespace std;

Fn main(int argc, char *argv[]) -> int:=

	cout << "counting a from 0 towards (and excluding) 5\n";
	For a:int(0)=>5 Do
	
		cout << "set a to " << a << endl;
		
		If a==0 Then
			cout << "a is 0\n";
		Endif
		
		If a==0 Then
			cout << "a is 0\n";
		Else
			cout << "a is not 0\n";
		Endif

		If a==0 Then
			cout << "a is 0\n";
		Elseif a==1 Then
			cout << "a is 1\n";
		Elseif a==2 Then
			cout << "a is 2\n";		
		Else
			cout << "a is not 0 or 1 or 2\n";
		Endif		
		
		\* °°this is a°° \* °°nested°° \* °°very nested°° *\*\
		°°multiline comment°° (I put the °° there to see if cpype wants to turn stuff into strings) *\
		
		Switch a
		Endswitch
		
		Switch a
			Default
				cout << "a is anything\n";
		Endswitch
		
		Switch a
			Case 0 Do
				cout << "a is 0\n";
		Endswitch

		Switch a
			Case 1,2,3 Do
				cout << "a is 1, 2 or 3\n";
		Endswitch

		Switch a
			Case 0 Do
				cout << "a is 0\n";
				Fall
		Endswitch		
		
		Switch a
			Case 0 Do
				cout << a;
				Fall
			Case 1, 2, 3 Do
				cout << "a is 1, 2 or 3 or maybe also 0\n";
			Default
				cout << "a ain't 0, 1, 2 or 3\n";;
		Endswitch
		
	Loop

	Var a=0; // auto
	Val c=0; // const auto
	
	While a<10 Do 
		a++;
	Loop
	cout << "a should be 10 and is " << a << endl;
	
	Repeat
		a++;
	Whilst a<20 Loop
	cout << "a should be 20 and is " << a << endl;
	
	Repeat
		a++;
	Until a==30 Loop
	cout << "a should be 30 and is " << a << endl;
	
	Var i = 0;
	cout << "outer scope i is " << i << endl;
	cout << "first 5 primes using inner scope i: ";
	For i:{2,3,5,7,11} Do
		cout << i << " "; 
	Loop
	cout << "\nouter scope i is " << i << endl;
	
	cout << "all combinations of (1, 2, 3) and (4, 5, 6): ";
	For x:{1,2,3}, y:{4,5,6} Do
		cout << x << y << " ";
	Loop
	cout << endl;

	vector<int> vi({1, 2, 3, 4});
	vector<int> vj({10, 20, 30, 40, 50, 60});
	
	cout << "elements in vi: ";
	For i:vi Do
		cout << i << " ";
	Loop
	cout << endl;

	cout << "copying all elements of vi onto some of vj\n";
	For [i:vi, j:vj] Do 
		j=i;
	Loop

	cout << "elements in vj: ";
	For j:vj Do
		cout << j << " ";
	Loop
	cout << endl;
	
	For [ei:vi, i:0...], [ej:vj, j:0...] Do
		cout << i << "th element of vi / " << j << "th element of vj = " << ei << "/" << ej << endl;
		If i==3 Then
			cout << "breaking nested loop\n";
			Break
		Endif
	Loop
	    
	cout << "Raw UTF8 String: " << °°Привет, мир!°° << endl;
	cout << "Mean escape tests: " << °°test°° << °°"\n° °° << "\"test\"" << "" "" << R"(test)" << R"//token(  test  )//token" << std::endl;
	
	
	voidFunctionWithoutNoParameters();
	voidFunctionWithNoParameters();
	cout << "7=" << inlineConstSeven() << endl;
	auto nismr = noInputSingleMultipleReturn();
	cout << "random value somewhere in memory: " << nismr.r << endl;
	auto nismdr = noInputSingleMultipleDefaultReturn();
	cout << "77: " << nismdr.r << endl;
	cout << "2 * 123 = " << twice(123) << endl;
	auto result = divWithRest(20, 3);
	cout << "20 = " << result.q << "*3 + " << result.r << endl;
	auto ab = fullMontyAndNicelyCommented(2);
	cout << "14=" << ab.a_new << ", 18=" << ab.b_new << endl;

	return 0;
Endfn


Fn voidFunctionWithoutNoParameters Endfn

Fn voidFunctionWithNoParameters() Endfn

Fn inlineConstSeven [inline const] -> int := return 7; Endfn

Fn noInputSingleMultipleReturn -> (int r) Endfn

Fn noInputSingleMultipleDefaultReturn -> (int r=77) Endfn

Fn twice (int x=0) -> int := return 2*x; Endfn

Fn divWithRest (int x=0, int y=1) -> (int q=x/y, int r=x%y) Endfn

Fn fullMontyAndNicelyCommented(
		int a=1, // first input parameter
		int b=2 // second input parameter
	) -> (
		int a_new=a, // first output parameter, default equal to input
		int b_new=b // second output parameter, default equal to input
	):=

	a_new *= 7;
	b_new *= 9;
	
	Return
	
	// this should not happen:
	a_new = 0;
	b_new = 0;
Endfn



