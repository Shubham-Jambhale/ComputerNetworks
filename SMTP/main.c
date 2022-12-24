#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int connect_smtp(const char* host, int port);
void send_smtp(int sock, const char* msg, char* resp, size_t len);



/*
  Use the provided 'connect_smtp' and 'send_smtp' functions
  to connect to the "lunar.open.sice.indian.edu" smtp relay
  and send the commands to write emails as described in the
  assignment wiki.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <email-to> <email-filepath>", argv[0]);
    return -1;
  }

  char* rcpt = argv[1];
  char* filepath = argv[2];



FILE *filePointer ;
     
    char source[4096];
    char dataToBeRead[4096];
 
    filePointer = fopen(filepath, "r") ;
    
    if ( filePointer == NULL )
    {
        printf( "Example.txt file failed to open." ) ;
    }
    else
    {  
        printf("The file is now opened.\n") ;
         
        while( fgets ( dataToBeRead,4096, filePointer ) != NULL )
        {
         
            strcat(source,dataToBeRead);
        }
        fclose(filePointer) ;
 
char *msg = malloc(strlen(source)+10);
strcpy(msg,source);
strcat(msg,"\r\n.\r\n");

char recpt[100];
sprintf(recpt,"RCPT TO:%s\n",rcpt);

char sendr[100];
sprintf(sendr,"MAIL FROM:%s\n",rcpt);

int socket = connect_smtp("lunar.open.sice.indiana.edu", 25);
char response[4096];

send_smtp(socket, "HELO client.example.com\n", response, 4096);
printf("%s\n", response);
send_smtp(socket, sendr, response, 4096);
printf("%s\n", response);
send_smtp(socket, recpt, response, 4096);
printf("%s\n", response);
send_smtp(socket,"DATA\n", response, 4096);
printf("%s\n", response);
send_smtp(socket, msg, response, 4096);
printf("%s\n", response);
send_smtp(socket, "QUIT\n", response, 4096);
printf("%s\n", response);

  return 0;
}

}