#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void send_http(char* host, char* msg, char* resp, size_t len);


/*
  Implement a program that takes a host, verb, and path and
  prints the contents of the response from the request
  represented by that request.
 */
int main(int argc, char* argv[]) {
  if (argc != 4) {
    printf("Invalid arguments - %s <host> <GET|POST> <path>\n", argv[0]);
    return -1;
  }
  char* host = argv[1];
  char* verb = argv[2];
  char* path = argv[3];


char *buf =malloc(strlen(argv[1])+strlen(argv[2])+50);  
strcpy(buf,verb);
strcat(buf," ");
strcat(buf, path);
strcat(buf, " HTTP/1.1\r\nHost:");
strcat(buf,host);
strcat(buf,"\r\n\r\n"); 

char response[4096];
send_http(host,buf, response,4096);
printf("%s\n", response);
  
  return 0;
}
