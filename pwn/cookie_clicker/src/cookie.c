#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <fcntl.h>

#define MAX_COOKIES 18000000000000000000UL
int stack_cookie;

void init(){
    srand(time(NULL));
    stack_cookie = rand();
    printf(" ____ ____ ____ _  ___ _____    \n");
    printf("/   _/  _ /  _ / |/ / /  __/    \n");
    printf("|  / | / \\| / \\|   /| |  \\      \n");
    printf("|  \\_| \\_/| \\_/|   \\| |  /_     \n");
    printf("\\____\\____\\____\\_|\\_\\_\\____\\____\n"); 
    printf("/   _/ \\  / /   _/ |/ /  __/  __\\\n");
    printf("|  / | |  | |  / |   /|  \\ |  \\/|\n");
    printf("|  \\_| |_/| |  \\_|   \\|  /_|    /\n");
    printf("\\____\\____\\_\\____\\_|\\_\\____\\_/\\_\\\n");
    sleep(5);
}

void clear(){
    for(int i = 0; i<0xff; i++){
        printf("\n");
    }
}

void flush(){
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

struct game_state{
    long unsigned int cookies;
    long unsigned int grandmas;
    long unsigned int active_rate;
    long unsigned int passive_rate;
};

long unsigned int cost(struct game_state *state){
    return 1000 + state->grandmas * state->passive_rate;
}

void io_loop(struct game_state *state){
    while(state->cookies < MAX_COOKIES){
        usleep(25000);
        clear();
        char selection;
        printf("\rCOOKIES: %lu\n", state->cookies);
        printf("GRANDMAS: %lu\n", state->grandmas);
        printf("COOKIES PER SECOND: %lu\n", state->passive_rate * state->grandmas * 100);
        printf("WIN CONDITION: %lu COOKIES\n\n", MAX_COOKIES);
        
        printf("MENU: \n");
        printf("1. Bake %lu cookies\n", state->active_rate);
        printf("2. Hire a grandma to bake %lu cookies per second [COST %lu COOKIES]\n", state->passive_rate * 100, cost(state));
        printf("3. Improve your baking rate by +100 cookies per click [COST %lu COOKIES]\n", cost(state));
        printf("4. Improve your grandmas baking rate by +100 cookies per second [COST %lu COOKIES]\n\n", cost(state));
        printf("Enter any key to refresh\n");
        scanf("%c", &selection);
        fflush(stdin);
        switch(selection){
            case '1':
                state->cookies += state->active_rate;
                break;
            case '2':
                state->cookies -= cost(state);
                state->grandmas += 1;
                break;
            case '3': 
               state->cookies -= cost(state);
               state->active_rate += 100;
               break;
            case '4':
               state->cookies -= cost(state);
               state->passive_rate += 1;
        }        
    }
}

void grandma_loop(struct game_state *state){
    while(state->cookies < MAX_COOKIES){
        usleep(10000);
        state->cookies += state->grandmas * state->passive_rate;
    }
}

void win(){
    flush();
    int local_stack_cookie = stack_cookie;
    char buf[20];
    printf("As a reward for beating cookie clicker, I will turn this into an easy buffer overflow challenge. Enter your payload!\n");
    fgets(buf, 100, stdin);
    if(local_stack_cookie != stack_cookie){
        printf("%d != %d\n", local_stack_cookie, stack_cookie);
        printf("STACK COOKIE MODIFIED, STACK OVERFLOW DETECTED.\n");
        printf("EXTREME SECURITY MEASURES ACTIVATED, SHUTTING DOWN POWER TO AWS-WEST\n");
        exit(-1);
    }
}

void print_flag(){
    int fd = open("./flag", O_RDONLY);
    char flag[100];
    read(fd, flag, 100);
    printf("%s\n", flag);
}

int main(){
    init();
    struct game_state state;
    state.cookies = 50000;
    state.active_rate = 100;
    state.passive_rate = 1;
    state.grandmas = 0;

    pthread_t thread_id[2];
    pthread_create(&thread_id[0], NULL, (void *)io_loop, (void *)&state);
    pthread_create(&thread_id[1], NULL, (void *)grandma_loop, (void *)&state);
    pthread_join(thread_id[0], NULL);
    pthread_join(thread_id[1], NULL);

    win();
}
