#include <structures.h>

// Types of token that are recognized by lexer
enum TOKEN_TYPES{
  TT_INT,
  TT_FLOAT,
  TT_PLUS,
  TT_MINUS,
  TT_MUL,
  TT_DIV,
  TT_LPARAN,
  TT_RPARAN,
};

// Creates list of tokens from text (Lexer)
struct token_list *make_tokens(char *text);
struct basic_return basic_run(char *fn, char * buff);
