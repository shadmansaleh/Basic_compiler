#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <basic.h>


int main()
{
  char *buff = (char*)malloc(1024 * sizeof(char));
  while(1){
    printf("Basic > ");
    scanf("%s", buff);
    if (strcmp(buff, "Exit") == 0) break;
    basic_run("<stdin>", buff);
  }
  free(buff);
  return 0;
}
