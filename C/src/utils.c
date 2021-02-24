#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <basic.h>
#include <utils.h>


char * str_enlarge(char * str, int size)
{
  char *new_str = (char*)malloc((strlen(str) + size) * sizeof(char));
  strcpy(new_str, str);
  free(str);
  return new_str;
}

char * str_shrink(char * str, int size)
{
  char *new_str = (char*)malloc(size * sizeof(char));
  strcpy(new_str, str);
  free(str);
  return new_str;
}

struct error_code *make_error(char* errro_type, char* fname,
    struct position* pos_start, char* error_details)
{
    char* error_msg = (char*)malloc((strlen(errro_type)
      + strlen(error_details + strlen(fname)) + 20) * sizeof(char));
    sprintf(error_msg, "%s:%s\nFile: %s, Line: %d", errro_type, error_details, fname, (pos_start->line_no + 1));
    // free(fname);
    // free(error_details);
    free(pos_start);
    struct error_code *return_val = (struct error_code*)malloc(sizeof(struct error_code));
    return_val->error_type = errro_type;
    return_val->error_msg = error_msg;
    return return_val;
}

size_t getline_from_text(char *text, struct position *pos, char *output, size_t len)
{
  int line_start = pos->idx - pos->column_no;
  int size = 0;
  for (size = 0; (text[size] != '\n' || text[size] != '\0') && size < len; ++size )
  {
    output[size] = text[line_start + size];
  }
  output[size] = '\0';
  return size;
}

void display_error(char *text, char *error_type, char *error_msg, struct position *pos)
{
  int len = 256;
  char *line = (char*)malloc(len * sizeof(char));
  line[0] = '\0';
  getline_from_text(text, pos, line, 256);
  printf("%s", line);
  free(line);
  for(int i=0; i < pos->column_no; ++i) putchar(' ');
  puts("^");
  printf("%s: File %s, Line %d\n%s",error_type, pos->file_name, pos->line_no + 1, error_msg);
}

void clear_token_list(struct token_list* tokens)
{
  if (!tokens) return;
  struct token_list *current = NULL;
  while (tokens != NULL) {
      current = tokens;
      if (tokens->token)
      {
        if (tokens->token->value != NULL)
        {
          free(tokens->token->value);
          tokens->token->value = NULL;
        }
        free(tokens->token);
        tokens->token = NULL;
      }
      tokens = tokens->next;
      free(current);
      current = NULL;
  }
  return;
}

void print_token(struct token* token)
{
  if (token == NULL) return;
  char * type_name;
  switch(token->type)
  {
    case TT_PLUS:
      printf("[PLUS, +]\n");
      break;
    case TT_MINUS:
      printf("[MINUS, -]\n");
      break;
    case TT_MUL:
      printf("[MUL, *]\n");
      break;
    case TT_DIV:
      printf("[DIV, /]\n");
      break;
    case TT_LPARAN:
      printf("[LPARAN, (]\n");
      break;
    case TT_RPARAN:
      printf("[RPARAN, )]\n");
      break;
    case TT_INT:
      printf("[INT, %i]\n", *(int*)token->value);
      break;
    case TT_FLOAT:
      printf("[FLOAT, %f]\n", *(float*)token->value);
      break;
  }
}

void print_token_list(struct token_list *tokens)
{
  if (!tokens) return;
  puts("{");
  while (tokens != NULL)
  {
    print_token(tokens->token);
    tokens = tokens->next;
  }
  puts("}");
  return;
}

