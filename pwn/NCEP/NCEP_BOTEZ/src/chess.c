#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>

#define READ 0
#define WRITE 1
#define BUFFER 0x100

struct __attribute__((__packed__)) gameInterface {
    int child_to_parent[2];
    int parent_to_child[2];
    char output_buffer[BUFFER];
    char input_buffer[BUFFER];
    char *command;
    pid_t pid;
};

void launch_gnuchess(struct gameInterface *game){
    if(pipe(game->child_to_parent) < 0){
        printf("error: could not open pipe\n");
        return;
    }
    if(pipe(game->parent_to_child) < 0){
        printf("error: could not open pipe\n");
        return;
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
        char *argv[] = {"/bin/bash", "-c", game->command, 0 }; 
        char *envp[] = {0};
        int ret = execve(argv[0], argv, envp);

        
        if(ret == -1)
            printf("execve error\n");
    }
    else{
        close(game->child_to_parent[WRITE]);
        close(game->parent_to_child[READ]);
    }
}

//reads output from gnuchess
void read_from_child(struct gameInterface *game){
    read(game->child_to_parent[READ], game->output_buffer, BUFFER);
}

//writes input to gnuchess
void write_to_child(struct gameInterface *game){
    write(game->parent_to_child[WRITE], game->input_buffer, strlen(game->input_buffer));
}

//gets input from stdin
void get_input(struct gameInterface *game){
    memset(game->input_buffer, 0, BUFFER);
    fgets(game->input_buffer, BUFFER * 5, stdin);
}

void * async_input(void *game){
    while(1){
        get_input((struct gameInterface *) game);
        write_to_child((struct gameInterface *) game);
    }
}

void * async_output(void *game){
    while(1){
        memset(((struct gameInterface *) game)->output_buffer, 0, BUFFER);
        read_from_child((struct gameInterface *) game);
        printf("%s", ((struct gameInterface *) game)->output_buffer);
    }
}

void thread_handler(struct gameInterface *game){
    int status;
    signal(SIGPIPE, SIG_IGN);
    pthread_t input_thread, output_thread;
    pthread_create(&input_thread, NULL, async_input, game);
    pthread_create(&output_thread, NULL, async_output, game);
    waitpid(game->pid, &status, 0);
    pthread_cancel(input_thread);
    pthread_join(input_thread, NULL);
    pthread_cancel(output_thread);
    pthread_join(output_thread, NULL);
}

char* load_flag(){
    int fd = open("./flag", O_RDONLY);
    char *flag = malloc(BUFFER);
    read(fd, flag, BUFFER);
    printf("flag loaded at %p\n", flag);
    close(fd);
    return flag;
}

void init_game(struct gameInterface *game){
    game->command = malloc(BUFFER);
    game->command = "/usr/games/gnuchess -g -m";
}

int main(){
    char *flag = load_flag();
    struct gameInterface *game = malloc(sizeof(struct gameInterface));
    init_game(game);
    printf("executing command: %s\n", game->command);
    launch_gnuchess(game);
    thread_handler(game);
    printf("finished executing command %s\n", game->command);
    free(game);
    free(flag);
    return 0;
}
