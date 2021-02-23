#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <basic.h>
#include <utils.h>


// Runs the lexer and prints tokens for now .
// Planed to work as base of parsing and execitimg in furture
struct basic_return basic_run(char *fn, char * buff)
{
  // gets token list from lexer
  struct token_list *tokens = make_tokens(buff);
  // prints token list
  print_token_list(tokens);
  clear_token_list(tokens);
  struct basic_return return_val;
  return return_val;
}
