#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

// COMPILE WITH
// cc -std=c99 -o testing testing
int main(void)
{    
    int pid;

    char *argsIn2[] = {
        "./mergetars",
        "testFiles/tarfiles/chrisCreate/monday.tar",
        "testFiles/tarfiles/testFiles1.tar",
        "testFiles/tarfiles/testFiles2.tgz",
        "testFiles/tarfiles/chrisCreate/tuesday.tar",        
        "testFiles/tarfiles/chrisCreate/wednesday.tgz",
        "testFiles/tarfiles/testFiles3.tar.gz",
        "testFiles/output/testOutput.tgz",
        NULL
    };
  
    //   char *argsIn2[] = {
    //     "./mergetars",
    //     "testFiles/tarfiles/testFiles1.tar",
    //     "testFiles/tarfiles/testFiles2.tgz",
    //     "testFiles/output/testOutput.tgz",
    //     NULL
    // };

    switch (pid = fork()) {
    case -1:
        printf("fork() failed\n");
        return 1;
    case 0:
        execlp("mkdir", "mkdir", "testFiles/output", NULL);
        break;
    default: {
        int status;
        wait(&status);
        }
    }

    switch (pid = fork()) {
    case -1:
        printf("fork() failed\n");
        return 1;
    case 0:
        execvp("./mergetars", argsIn2);
        break;
    default: {
        int status;
        wait(&status);
        }
    }

    // switch (pid = fork()) {
    // case -1:
    //     printf("fork() failed\n");
    //     return 1;
    // case 0:
    //     execlp("tar", "tar", "-xzf", "testFiles/output/testOutput.tgz", "-C", "testFiles/output", NULL);
    //     // execlp("tar", "tar", "-xzf", "testFiles/output/testOutput.tgz", "-C", "testFiles/output", NULL);
    //     break;
    // default: {
    //     int status;
    //     wait(&status);
    //     }
    // }


    // switch (pid = fork()) {
    // case -1:
    //     printf("fork() failed\n");
    //     return 1;
    // case 0:
    //     execlp("tree", "tree", "-Dh", "testFiles/output", NULL);
    //     break;
    // default: {
    //     int status;
    //     wait(&status);
    //     }
    // }

    // // switch (pid = fork()) {
    // // case -1:
    // //     printf("fork() failed\n");
    // //     return 1;
    // // case 0:
    // //     system("rm -rf testFiles/output/testOutput.tgz");
    // //     break;
    // // default: {
    // //     int status;
    // //     wait(&status);
    // //     }
    // // }

    // // switch (pid = fork()) {
    // // case -1:
    // //     printf("fork() failed\n");
    // //     return 1;
    // // case 0:
    // //     system("rm -rf testFiles/output");
    // //     break;
    // // default: {
    // //     int status;
    // //     wait(&status);
    // //     }
    // // }


    return 0;
}

