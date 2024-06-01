/*  CITS2002 Project 2 2020
    Name:               Thomas Cleary
    Student Number:     21704985
*/

#include <stdio.h>          //  BUFSIZ, printf(), perror(), sprintf(), snprintf(),
                            //  fopen(), fread(), fwrite(), fclose(), remove()

#include <stdlib.h>         //  EXIT_FAILURE, EXIT_SUCCESS, exit(), free(),
                            //  malloc(), calloc(), mkdtemp(linux)

#include <unistd.h>         //  fork(), execlp(), mkdtemp(macOS) 

#include <string.h>         //  strdup(), strrchr(), strcmp()

#include <dirent.h>         //  opendir(), readdir()

#include <stdbool.h>        //  true, false

#include <sys/stat.h>       //  S_ISIDR, S_ISREG, stat(), mkdir(), chmod()

#include <sys/types.h>      //  mode_t, size_t

#include <sys/param.h>      //  MAXPATHLEN

#include <sys/time.h>       //  struct timeval, utimes()

#include <sys/wait.h>       //  wait()


//  required for mkdtemp() on linux
#define _POSIX_C_SOURCE 200809L

//  required to run below functions on linux
#if defined(__linux__)
extern  char    *mkdtemp(char *template);
extern  char    *strdup(const char *str);
#endif


//  MERGE_INFO holds all required file path information
typedef struct {

    char    *tempParentPath;
    char   **extractedTarPaths;
    char    *tempOutPath;
    char    *requestedOutPath;

    int      numInTarfiles;
    int      numExtracted;

} MERGE_INFO;


//  mergetars.c
void mergetars(int, char *[]);

//  mergeInfo.c
extern MERGE_INFO   *initMergeInfo(int, char*[]);
extern void          freeMergeInfo(MERGE_INFO *);

//  tarfileHandling.c
extern char         *extractTarfile(char *, char *);
extern void          createTarfile(char *, char *, char *);

//  fileHandling.c
extern char         *makeTempDir(char *);
extern void          makeDir(char *, mode_t);
extern void          copyFile(char *, char *, struct timeval[], mode_t);
extern void          removeFile(char *);
extern bool          isValidFilename(char *);
extern void          removeDir(char *);

//  addFiles.c
extern void          addFiles(char *, char *);

//  errors.c
extern void          errorExit(char *);
extern void          argNumHelp(int);
extern void          inputHelp(void);
extern void          nullCheck(void *);
extern void          nonZeroCheck(int);
extern void          pathLengthCheck(int, char *);
extern void          strrchrCheck(char *, char *);
extern void          fReadWriteCheck(int, int);
extern void          forkError(void);
extern void          tarCheck(int, char *);
