#include <stdio.h>
#include <fcntl.h> 

void win(){
    char shellcode[1000];
    printf("nice! I'll execute any shellcode you give me now\n");
    fgets(shellcode, 1000, stdin);
    void (*fun_ptr)(void) = shellcode;
    (*fun_ptr)();
}

void part2(){
    char buf[20];
    printf("This is a review challenge, you know the drill\n");
    printf("Return to the win function and get the flag\n");
    fgets(buf, 100, stdin);
    return;
}


int main(){
    part2();
}
