// Utility functions that doesn't make much sence anywhere else

// Increases strs size by size from current len(frees str)
char * str_enlarge(char * str, int size);
// limists strss size to size(frees str)
char * str_shrink(char * str, int size);
// Genarates errors
struct error_code *make_error(char* errro_type, char* fname,
    struct position* pos_start, char* error_details);
// frees tokens
void clear_token_list(struct token_list * token);
// prints a token
void print_token(struct token* token);
// prints ei\ntire list of tokens
void print_token_list(struct token_list *tokens);
void display_error(char *text, char *error_type, char *error_msg, struct position *pos);
