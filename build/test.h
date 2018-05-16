// test.h
//

#ifndef LZZ_test_h
#define LZZ_test_h
#include "cpype.h"
#include<iostream>
#include<cstdlib>
#include<vector>
#define LZZ_INLINE inline
int main (int argc, char * (argv) []);
void f1 ();
void f2 ();
int f3 ();
int const f35 ();
struct f4__result
{
  int r;
};
f4__result f4 ();
void f5 ();
struct f6__result
{
  int q;
  int r;
};
f6__result const f6 (int x = 0, int y = 1);
struct f7__result
{
  int a_new;
  int b_new;
};
f7__result f7 (int a = 1, int b = 2 /* second input parameter*/);
LZZ_INLINE int const f35 ()
                       {}
LZZ_INLINE f6__result const f6 (int x, int y)
                                            {
	int q=x/y;
	int r=x%y;
	return {q, r};
}
#undef LZZ_INLINE
#endif
