#hdr
#include<iostream>
#include<cstdlib>
#include<vector>
#end

using namespace std;

Fn main(int argc, char *argv[]) -> int:=

	int a=0, b=0;

	
	If a==0 Then
		cout << "a is 0";
	Endif
	
	If a==0 Then
		cout << "a is 0";
	Else
		cout << "a is not 0";
	Endif

	If a==0 Then
		cout << "a is 0";
	Elseif a==1 Then
		cout << "a is 1";
	Elseif a==2 Then
		cout << "a is 2";		
	Else
		cout << "a is not 0 or 1 or 2";
	Endif		
	
	\* °°this is a°° \* °°nested°° \* °°very nested°° *\*\
	°°multiline comment°° *\
	
	Switch a
	Endswitch
	
	Switch a
		Default
			cout << a;
	Endswitch
	
	Switch a
		Case 0 Do
			cout << a;
	Endswitch

	Switch a
		Case 1,2,3 Do
			cout << a;
	Endswitch

	Switch a
		Case 0 Do
			cout << a;
			Fall
	Endswitch		
	
	Switch a
		Case 0 Do
			cout << a;
			Fall
		Case 1, 2, 3 Do
			cout << a;
		Default
			cout << a;
	Endswitch
	
	 
	While b<10 Do 
		b++;
	Loop
	
	Repeat
		b++;
	Whilst b<20 Loop
	
	Repeat
		b++;
	Until b==30 Loop 
	

	For i:{1,2,3} Do
		cout << i; 
	Loop
	
	For x:{1,2,3}, y:{4,5,6} Do
		cout << x << y;
	Loop

	vector<int> vi({15,16,17,18});
	vector<int> vj({25,26,27,28,29});
	For i:vi Do
		cout << i;
	Loop
	
	For [i:vi, j:vj] Do
		j=i;
	Loop
	
	For x:{1,2,3}, y:{4,5,6}, [i:vi, j:vj] Do
		j=i;
	Loop

	For [i:1->5, j:1... ] Do
	Loop
	
	cout << °°test°° << °°°° << "\"test\"" << "" "" << R"(test)" << R"/token(  test  )/token" << std::endl;
	system("pause");
	
	return 0;
Endfn


Fn f1 Endfn

Fn f2() Endfn

Fn f3 -> int Endfn

Fn f35 [inline const] -> int Endfn

Fn f4 -> (int r) Endfn

Fn f5:= return 0; Endfn

Fn f6[inline const](int x=0, int y=1) -> (int q=x/y, int r=x%y) Endfn

Fn f7( // nicely commented function
		int a=1, // first input parameter
		int b=2 // second input parameter
	) -> (
		int a_new=a, // first output parameter, default equal to input
		int b_new=b // second output parameter, default equal to input
	):=

	a_new *= 17;
	b_new *= 19;
	
	Return
	
	a_new = 0;
	b_new = 0;
Endfn


