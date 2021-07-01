#include <stdio.h>
#include<fcntl.h> 
struct __attribute__((__packed__)) Val{
    char buf[20];
    __uint64_t secret_value;
};

void win(){
    char flag[100];
    int fd = open("./flag", O_RDONLY);
    read(fd, flag, 100);
    printf("%s\n", flag);
}

void part2(){
    char buf[20];
    printf("Well done!\n");
    printf("That was the same vuln as last week though, we probably shouldn't give you a flag for that\n");
    printf("Reply \"yes\" to awknowledge that you don't deserve any points\n");
    fgets(buf, 100, stdin);
    return;
}

void part1(){
    struct Val v;
    v.secret_value = 0;
    printf("Reply \"yes\" if you remember how to overwrite data\n");
    fgets(v.buf, 32, stdin);
    if(v.secret_value == 0xbaddecafbeefcafe){
        part2();
    }
    return;
}

int main(){
    part1();
}
