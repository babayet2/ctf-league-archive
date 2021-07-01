#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <sched.h>
#include <time.h>


#define READ 0
#define WRITE 1
#define BUFFER 0x500
#define MAX_GAMES 10
#define MAX_LOGS 50

pthread_mutex_t input_lock;
pthread_mutex_t output_lock;

struct __attribute__((__packed__)) gameInterface {
    int child_to_parent[2];
    int parent_to_child[2];
    char output_buffer[BUFFER];
    char input_buffer[BUFFER];
    char command[BUFFER];
    pid_t pid;
};

struct __attribute__((__packed__)) debug_log {
    time_t time_initiated;
    time_t time_ended;
    char description[BUFFER * 3];
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

    fcntl(game->child_to_parent[READ], F_SETFL, O_NONBLOCK);

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
        pthread_mutex_lock(&input_lock);
        struct gameInterface *current_game = *((struct gameInterface **) game);
        get_input(current_game);
        write_to_child(current_game);
        pthread_mutex_unlock(&input_lock);
        usleep(2000);
    }
}

void * async_output(void *game){
    while(1){
        pthread_mutex_lock(&output_lock);
        struct gameInterface *current_game = *((struct gameInterface **) game);
        read_from_child(current_game);
        printf("%s", current_game->output_buffer);
        memset(current_game->output_buffer, 0, BUFFER);
        pthread_mutex_unlock(&output_lock);
    }
}

void *thread_handler(void *current_game){
    printf("starting thread handler\n");
    int status;
    pthread_t input_thread, output_thread;
    pthread_create(&input_thread, NULL, async_input, current_game);
    pthread_create(&output_thread, NULL, async_output, current_game);
    //TODO fix this
    while(1);
    //waitpid(game->pid, &status, 0);
    pthread_cancel(input_thread);
    pthread_join(input_thread, NULL);
    pthread_cancel(output_thread);
    pthread_join(output_thread, NULL);
    printf("ending thread handler\n");
}

void print_log(struct debug_log *log){
    printf("PID\n%d\n", log->pid);
    printf("TIME INITIATED: %ld\n", log->time_initiated);
    printf("DESCRIPTION: %s\n", log->description);
}

void edit_logs(struct debug_log **logs, int num_logs){
    char buf[10];
    int log_id;
    int selection;
    printf("ENTER THE ID OF THE LOG YOU WOULD LIKE TO EDIT: ");
    fgets(buf, 10, stdin);
    sscanf(buf, "%d ", &log_id);
    
    if(log_id < 0 || log_id >= num_logs){
        printf("INVALID LOG ID\n");
        return;
    }

    printf("LOG UPDATE MENU:\n");
    printf("1. UPDATE PROCESS ID\n");
    printf("2. UPDATE START TIME\n");
    printf("3. UPDATE END TIME\n");
    printf("4. UPDATE DESCRIPTION\n");
    
    fgets(buf, 10, stdin);
    sscanf(buf, "%d ", &selection);

    switch(selection){
        case 1:
            printf("ENTER A NEW PID: ");
            fgets(buf, 10, stdin);
            sscanf(buf, "%d ", &logs[log_id]->pid);
            break;
        case 2:
            printf("ENTER A NEW UNIX TIMESTAMP: ");
            fgets(buf, 10, stdin);
            sscanf(buf, "%ld ", &logs[log_id]->time_initiated);
            break;
        case 3:
            printf("ENTER A NEW UNIX TIMESTAMP: ");
            fgets(buf, 10, stdin);
            sscanf(buf, "%ld ", &logs[log_id]->time_ended);
            break;
        case 4:
            printf("ENTER A NEW DESCRIPTION: ");
            fgets(logs[log_id]->description, BUFFER*3, stdin);
            break;
    }
}

void log_menu(struct debug_log **logs, int *num_logs){
    char buf[10];
    int log_id;
    int selection;
    while(1){
        printf("LOGGING MENU\n");
        printf("1. VIEW PROCESS LOGS\n");
        printf("2. ADD PROCESS LOG\n");
        printf("3. EDIT PROCESS LOG\n");
        printf("4. DELETE PROCESS LOG\n");
        printf("5. EXIT\n");
        printf("ENTER A MENU SELECTION: ");
        fgets(buf, 10, stdin);
        sscanf(buf, "%d ", &selection);
        switch(selection){
            case 1:
                for(int i = 0; i < *num_logs; i++){
                    printf("LOG #%d:\n", i);
                    print_log(logs[i]);
                }
                break;
            case 2:
                if(*num_logs < MAX_LOGS){
                    logs[*num_logs] = malloc(sizeof(struct debug_log));
                    memset(logs[*num_logs], 0, sizeof(struct debug_log));
                    printf("LOG #%d CREATED\n", *num_logs);
                    *num_logs += 1;
                }
                else{
                    printf("ERROR: TOO MANY LOGS, CANNOT ADD TO LIST\n");
                }
                break;
            case 3:
                edit_logs(logs, *num_logs);
                break;
            case 4:
                printf("ENTER THE ID OF THE LOG YOU WOULD LIKE TO DELETE: ");
                fgets(buf, 10, stdin);
                sscanf(buf, "%d ", &log_id);
                if(log_id < 0 || log_id >= *num_logs){
                    printf("INVALID LOG ID\n");
                    break;
                }
                struct debug_log *temp = logs[log_id];
                *num_logs -= 1;
                logs[log_id] = logs[*num_logs];
                free(logs[*num_logs]);
                break;
            case 5:
                return;
        }
    }
}

void edit_game(struct gameInterface *game){
    char buf[BUFFER];
    printf("ENTER YOUR LAUNCH COMMAND: ");
    fgets(buf, BUFFER, stdin);
    if(strcmp(buf, "/usr/games/gnuchess -g -m")){
        printf("INVALID LAUNCH COMMAND, DISCARDING\n");
        return;
    }
    strncpy(game->command, buf, BUFFER);
}

void process_menu(struct gameInterface **games, int *num_games){
    char buf[10];
    int log_id;
    int selection;
    struct gameInterface *new_game = NULL;
    while(1){
        printf("NEW PROCESS MENU\n");
        printf("1. ALLOCATE A NEW PROCESS\n");
        printf("2. EDIT YOUR NEW PROCESS\n");
        printf("3. ADD NEW PROCESS TO THE SCHEDULE\n");
        printf("4. EXIT\n");
        printf("ENTER A MENU SELECTION: ");
        fgets(buf, 10, stdin);
        sscanf(buf, "%d ", &selection);
        switch(selection){
            case 1:
                if(*num_games < MAX_GAMES){
                    new_game = malloc(sizeof(struct gameInterface));
                    printf("PROCESS CREATED!\n");
                }
                else{
                    printf("ERROR: TOO MANY PROCESSES, CANNOT CREATE A NEW ONE\n");
                }
                break;
            case 2:
                edit_game(new_game);
                break;
            case 3:
                launch_gnuchess(new_game);
                games[*num_games] = new_game;
                *num_games += 1;
                printf("SUCCESS: PROCESS ADDED TO SCHEDULE\n");
                return;
            case 4:
                return;
        }
    }
}

void scheduler(){
    int num_games = 5;
    int num_logs = 5;
    struct gameInterface **games = malloc(sizeof(struct gameInterface *) * MAX_GAMES);
    struct debug_log **logs = malloc(sizeof(struct debug_log *) * MAX_LOGS);


    for(int i = 0; i < num_games; i++){
        games[i] = malloc(sizeof(struct gameInterface));
        sprintf(games[i]->command, "/usr/games/gnuchess -g -m");
        launch_gnuchess(games[i]);
        
        logs[i] = malloc(sizeof(struct debug_log));
        sprintf(logs[i]->description, "A gnuchess process, launched at start of the wrapper\n");
        logs[i]->time_initiated = time(0);
        logs[i]->time_ended = 0;
        logs[i]->pid = games[i]->pid;
    }

    struct gameInterface *current_game = games[0];
    pthread_t io_threads;
    pthread_create(&io_threads, NULL, thread_handler, &current_game);
    int iteration = 0;
    while(1){
        int game = iteration % num_games;
        pthread_mutex_lock(&input_lock);
        pthread_mutex_lock(&output_lock);
        printf("\n==========CONTEXT SWITCH: GAME #%d HAS BEEN SCHEDULED==========\n", game);
        if(strstr(current_game->input_buffer, "INT1")){
            log_menu(logs, &num_logs);
        }
        if(strstr(current_game->input_buffer, "INT2")){
            process_menu(games, &num_games);
        }
        current_game = games[game];
        pthread_mutex_unlock(&input_lock);
        pthread_mutex_unlock(&output_lock);
        sleep(5);
        iteration++;
    }
}   

int main(){
    scheduler();
    return 0;
}
