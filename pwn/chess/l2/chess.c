#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <signal.h>
#include <sys/types.h>

#define READ 0
#define WRITE 1
#define BUFFER 0xFF

struct gameInterface {
    int child_to_parent[2];
    int parent_to_child[2];
    char input_buffer[BUFFER];
    char output_buffer[BUFFER];
    pid_t pid;
};

int launch_gnuchess(struct gameInterface *game, char *launch_string){
    if(pipe(game->child_to_parent) < 0){
        printf("error: could not open pipe\n");
        return -1;
    }
    if(pipe(game->parent_to_child) < 0){
        printf("error: could not open pipe\n");
        return -1;
    }

    game->pid = fork();

    if(game->pid == 0){
        //close unnecessary ends of the pipe
        close(game->child_to_parent[READ]);
        close(game->parent_to_child[WRITE]);
    
        //create new stdin
        close(0);
        int new_stdin = dup(game->parent_to_child[READ]);
        if(new_stdin < 0){
            printf("error: could not dup stdin for child\n");
        }
        close(1);
        int new_stdout = dup(game->child_to_parent[WRITE]);
        if(new_stdout < 0){
            printf("error: could not dup stdout for child\n");
        }
        char *argv[] = {"/bin/bash", "-c", launch_string, 0 }; 
        char *envp[] = {0};
        int ret = execve(argv[0], argv, envp);

        
        if(ret == -1)
            printf("execve error\n");
    }
    else{
        close(game->child_to_parent[WRITE]);
        close(game->parent_to_child[READ]);
        return 0;
    }
    return -1;
}

//reads output from gnuchess
int read_from_child(struct gameInterface *game, int timeout){
    read(game->child_to_parent[READ], game->output_buffer, BUFFER);
    return 0;
}

//writes input to gnuchess
int write_to_child(struct gameInterface *game){
    write(game->parent_to_child[WRITE], game->input_buffer, strlen(game->input_buffer));
    return 0;
}

//gets input from stdin
int get_input(struct gameInterface *game){
    memset(game->input_buffer, 0, BUFFER);
    fgets(game->input_buffer, BUFFER, stdin);
}

void * async_input(void *game){
    //while(kill(((struct gameInterface *)game)->pid >= 0, 0)){
    while(1){
        get_input((struct gameInterface *) game);
        write_to_child((struct gameInterface *) game);
    }
}

void * async_output(void *game){
    while(1){
        memset(((struct gameInterface *) game)->output_buffer, 0, BUFFER);
        read_from_child((struct gameInterface *) game, 100);
        printf("%s", ((struct gameInterface *) game)->output_buffer);
    }
}

int main(){
    struct gameInterface game;
    char arguments[0x50];
    char launch_string[0x100];
    printf("Whoa that was dumb... I'll sanitize the input this time\n");
    fgets(arguments, 0x50, stdin);
    snprintf(launch_string, 0x100, "/usr/local/bin/gnuchess %s", arguments);
    printf("launching: %s", launch_string);
    launch_gnuchess(&game, launch_string);
    read_from_child(&game, 2);
    printf("%s", game.output_buffer);
    pthread_t input_thread, output_thread;
    pthread_create(&input_thread, NULL, async_input, &game);
    pthread_create(&output_thread, NULL, async_output, &game);
    pthread_join(input_thread, NULL);
    return 0;
}
