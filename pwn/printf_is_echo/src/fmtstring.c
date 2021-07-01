#include <stdio.h>
#include <fcntl.h> 
#include <string.h>

struct __attribute__((__packed__)) Val{
    char buf[0x50];
    __uint64_t secret_value;
};

void win(){
    char flag[100];
    int fd = open("./flag", O_RDONLY);
    read(fd, flag, 100);
    printf("%s\n", flag);
}

int echo(){
    struct Val v;
    v.secret_value = (__uint64_t) &win;

    //memset(buf, '\0', 0x20);
    printf("did you know the unix tool echo can be implemented with two lines of C? I'll echo some bytes, try it!\n");
 
    fgets(v.buf, 0x49, stdin);
    printf(v.buf);

    printf("\nI used ASLR (with PIE), so the address of the win function is randomized!\n");
    printf("I'll give you the last three hex digits of the address as a hint: %p\n", v.secret_value & 0xfff);
    printf("Type \"I give up\" to acknowledge that this binary is unhackable\n");
    fgets(v.buf, 0x200, stdin);
    return 0;
}

int main(){
    echo();
}

