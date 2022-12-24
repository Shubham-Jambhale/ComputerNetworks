#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string.h>

/*
  Use the `getaddrinfo` and `inet_ntop` functions to convert a string host and
  integer port into a string dotted ip address and port.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <host> <port>", argv[0]);
    return -1;
  }
  char* host = argv[1];
  long port = atoi(argv[2]);
  (void) port;

  struct addrinfo hints, *res=NULL;
/* This code of hints is referred from lab 4 computer networks*/
  memset(&hints, 0, sizeof(hints));
  hints.ai_flags    = AI_PASSIVE;
  hints.ai_family   = AF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_protocol = IPPROTO_TCP;


getaddrinfo(host,"http",&hints, &res);
struct addrinfo* i;
char buff[200];

for(i=res ; i!= NULL ;i=i->ai_next)
{

/* This code is referred from course github repo*/
void* raw_addr;
if (i->ai_family == AF_INET) { // Address is IPv4
  struct sockaddr_in* tmp = (struct sockaddr_in*)i->ai_addr; // Cast addr into AF_INET container
  raw_addr = &(tmp->sin_addr); // Extract the address from the container
  inet_ntop(AF_INET,raw_addr,buff,sizeof(buff));
  printf("IPv4 %s\n",buff);
}
else { // Address is IPv6
  struct sockaddr_in6* tmp = (struct sockaddr_in6*)i->ai_addr; // Cast addr into AF_INET6 container
  raw_addr = &(tmp->sin6_addr); // Extract the address from the container
  inet_ntop(AF_INET6,raw_addr,buff,sizeof(buff));
  printf("IPv6 %s\n",buff);
}

}


  return 0;
}
