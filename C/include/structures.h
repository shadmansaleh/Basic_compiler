// Token
struct token{
  int type;
  void *value;
};

// Linked list of tokens
struct token_list{
  struct token *token;
  struct token_list *next;
};

// Error code to be sent to main
struct error_code{
  char *error_type;
  char *error_msg;
};

struct basic_return{
  struct token *token_list;
  struct error_code error_msg;
};

// Stores position of lexer
struct position {
  int idx;
  int line_no;
  int column_no;
  char current_char;
  char *file_name;
};
