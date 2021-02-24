#include <basic.h>
#include <utils.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

struct token *make_number(char * text, struct position *pos);
void advance_position(struct position *pos, char *text);
struct token_list *add_token(struct token_list *last_entry, 
    int token_type, void *token_val);

// Creates a lint of tokens from text
struct token_list *make_tokens(char *text, char *fname)
{
  // Preparation
  struct token_list *first_item = (struct token_list*)malloc(sizeof(struct token_list));
  first_item->token = NULL;
  first_item->next = NULL;
  struct token_list *last_item = first_item;
  struct token_list *second_last_item = last_item;
  struct position pos;
  pos.idx = 0;
  pos.column_no = 0;
  pos.line_no = 0;
  pos.current_char = text[pos.idx];
  pos.file_name = fname;
  int has_ended = 0;
  while(pos.current_char != '\0' && !has_ended){
    if (isspace(pos.current_char)) advance_position(&pos, text);
    else if (isdigit(pos.current_char)) {
      struct token* token = make_number(text, &pos);
      struct token_list *new = (struct token_list*)malloc(sizeof(struct token_list));
      last_item->token = token;
      last_item->next = new;
      second_last_item = last_item;
      last_item = new;
    }else if (pos.current_char == '+') {
      second_last_item = last_item;
      last_item = add_token(last_item, TT_PLUS, NULL);
      advance_position(&pos, text);
    }else if (pos.current_char == '-') {
      second_last_item = last_item;
      last_item = add_token(last_item, TT_MINUS, NULL);
      advance_position(&pos, text);
    }else if (pos.current_char == '*') {
      second_last_item = last_item;
      last_item = add_token(last_item, TT_MUL, NULL);
      advance_position(&pos, text);
    }else if (pos.current_char == '/') {
      second_last_item = last_item;
      last_item = add_token(last_item, TT_DIV, NULL);
      advance_position(&pos, text);
    }else if (pos.current_char == '(') {
      second_last_item = last_item;
      last_item = add_token(last_item, TT_LPARAN, NULL);
      advance_position(&pos, text);
    }else if (pos.current_char == ')') {
      second_last_item = last_item;
      last_item = add_token(last_item, TT_RPARAN, NULL);
      advance_position(&pos, text);
    }else{
      char msg[50];
      sprintf(msg, "Error in tokenizer %c not expected\n", pos.current_char);
      display_error(text, "Unknown Character", msg, &pos);
      advance_position(&pos, text);
      if (last_item != first_item) free(last_item);
      second_last_item->next = NULL;
      clear_token_list(first_item);
      return NULL;
    }
  }
  free(last_item);
  second_last_item->next = NULL;
  return first_item;
}


// Increases position of lexer
void advance_position(struct position *pos, char *text)
{
  pos->idx += 1;
  pos->column_no += 1;
  pos->current_char = text[pos->idx];
  if (pos->current_char == '\n')
  {
    pos->column_no = 0;
    pos->line_no += 1;
  }
  return;
}

// Extracts ints and floats from text
struct token *make_number(char * text, struct position *pos)
{
  struct token *token = (struct token*)malloc(sizeof(struct token));
  int size = 100;
  int len = 0;
  int dot_count = 0;
  char *num_str = (char*)malloc(size * sizeof(char));
  *num_str='\0';
  int has_ended = 0;
  while (pos->current_char != '\0' && !has_ended){
    switch(pos->current_char)
    {
      case '0':
      case '1':
      case '2':
      case '3':
      case '4':
      case '5':
      case '6':
      case '7':
      case '8':
      case '9':
        num_str[len] = pos->current_char;
        len += 1;
        advance_position(pos, text);
        break;
      case '.':
        if (dot_count == 0)
        {
          dot_count += 1;
          num_str[len] = pos->current_char;
          len += 1;
          advance_position(pos, text);
          break;
        }else{
          dot_count += 1;
            has_ended = 1;
          free(num_str);
          num_str = NULL;
        }
        break;
      default:
        num_str[len] = '\0';
        has_ended = 1;
        break;
    }
  }
  if (num_str != NULL)
  {
    if (dot_count == 0)
    {
      token->type = TT_INT;
      int *num = (int*)malloc(sizeof(int));
      *num = atoi(num_str);
      token->value = (void*)num;
    }else{
      token->type = TT_FLOAT;
      float *num = (float*)malloc(sizeof(float));
      *num = atof(num_str);
      token->value = (void*)num;
    }
    free(num_str);
    num_str = NULL;
  }
  return token;
}


// Addes token to token list
struct token_list *add_token(struct token_list *last_entry, int token_type, void *token_val)
{
  struct token *token = (struct token*)malloc(sizeof(struct token));
  struct token_list *new = (struct token_list*)malloc(sizeof(struct token_list));
  token->type = token_type;
  token->value = token_val;
  last_entry->token = token;
  last_entry->next = new;
  return new;
}

