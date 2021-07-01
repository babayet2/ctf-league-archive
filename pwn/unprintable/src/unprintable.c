#include <stdio.h>

void input() {
    char shellcode[100];

    printf("Here's your special RAM, happy birthday!: %p\n", &shellcode);
    puts("What are you going to do with it?");

    gets(shellcode);
}

int main() {
    puts("I found some empty room in the RAM on this system, and prepared some especially for you!");
    puts("But I'm worried you might put something evil in it, so I'm not going to print it out");

    input();

    puts("I hope you enjoyed your memory!");
}
