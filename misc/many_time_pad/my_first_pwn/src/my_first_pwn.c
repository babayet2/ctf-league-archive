#include <stdio.h>
#include<fcntl.h> 
#include <string.h>

void print_the_flag(){
    char flag[100];
    int fd = open("./flag", O_RDONLY);
    read(fd, flag, 100);
    printf("%s\n", flag);
}

int check_the_key(){
    char secret_key[512];
    char user_input[512];
    printf("enter the secret key from the web portion of this challenge\n");
    int fd = open("./secret_key.txt", O_RDONLY);
    read(fd, secret_key, 257);
    fgets(user_input, 257, stdin);
    return strncmp(secret_key, user_input, 256);
}

int main(){
    char buf[16];
    if(check_the_key()) return;
    printf("overflow my buffer and return to the print_the_flag function\n");
    fgets(buf, 32, stdin);
}
