#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <basic.h>


int main()
{
  char *buff = (char*)malloc(1024 * sizeof(char));
  printf("Basic > ");
  while(fgets(buff, 1024, stdin))
  {
    // Main loop
    if (strcmp(buff, "Exit\n") == 0) break;
    basic_run("<stdin>", buff);
    printf("Basic > ");
  }
  free(buff);
  return 0;
}
