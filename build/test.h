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
void voidFunctionWithoutNoParameters ();
void voidFunctionWithNoParameters ();
int const inlineConstSeven ();
struct noInputSingleMultipleReturn__result
{
  int r;
};
noInputSingleMultipleReturn__result noInputSingleMultipleReturn ();
struct noInputSingleMultipleDefaultReturn__result
{
  int r;
};
noInputSingleMultipleDefaultReturn__result noInputSingleMultipleDefaultReturn ();
int twice (int x = 0);
struct divWithRest__result
{
  int q;
  int r;
};
divWithRest__result divWithRest (int x = 0, int y = 1);
struct fullMontyAndNicelyCommented__result
{
  int a_new;
  int b_new;
};
fullMontyAndNicelyCommented__result fullMontyAndNicelyCommented (int a = 1, int b = 2 /* second input parameter*/);
LZZ_INLINE int const inlineConstSeven ()
                                    {
	return 7; 
}
#undef LZZ_INLINE
#endif
