#include <stdio.h>
#include<fcntl.h> 
char flag[100];

struct Val{
    char buf[20];
    __uint64_t current_count;
    __uint64_t max;
};

int main(){
    printf("HOW FAST CAN YOU PRESS ENTER???\n");
    struct Val v;
    v.max = -1;
    v.current_count = 0;
    
    while(v.current_count < v.max){
        printf("PRESS ENTER TO COUNT UP, FLAG WHEN CURRENT COUNT == %#016lx\nCURRENT COUNT: %#016lx\n", v.max, v.current_count);
        v.current_count++;
        fgets(v.buf, 0x100, stdin);
    }

    int fd = open("./flag", O_RDONLY);
    read(fd, flag, 100);
    printf("%s\n", flag);
}
