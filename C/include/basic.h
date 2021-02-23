struct token{
  char *type;
  void *val;
};

struct error_code{
  char *error_type;
  char *error_msg;
};

struct basic_return{
  struct token *token_list;
  struct error_code error_msg;
};

basic_return basic_run(char *fn, char * buff);

