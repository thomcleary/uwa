/*  CITS2002 Project 2 2020
    Name:               Thomas Cleary
    Student Number:     21704985
*/

#include "mergetars.h"


//  return the string of switches that the tar command should use on tarFileName
char *getTarSwitches(char *tarfileName, bool extract)
{
    char *switches = NULL;

    //  looking for ".gz", ".tgz", ".tar"
    //  NOTE: for ".tar.gz" project spec guarantees correct tarfile paths so only need to find ".gz" 
    char *fileType = strrchr(tarfileName, '.');
    strrchrCheck(tarfileName, fileType);

    //  if tarFileName is uncompressed
    if (strcmp(fileType, ".tar") == 0) {
        if (extract)    switches = strdup("-xpf");  //  extract, preserve-permissions, file
        else            switches = strdup("-cpf");  //  create,  preserve-permissions, file
    }
    //  if tarFileName is compressed
    else if (strcmp(fileType, ".gz") == 0 || strcmp(fileType, ".tgz") == 0)  {
        if (extract)    switches = strdup("-xpzf"); //  extract, preserve-permissions, gzip, file
        else            switches = strdup("-cpzf"); //  create,  preserve-permissions, gzip, file
    }
    //  for completeness (project spec guarantees correct cmd line inputs) (should do this before calling mergetars())
    else {
        char message[BUFSIZ];
        snprintf(message, BUFSIZ, "file '%s' has incorrect filetype '%s'", tarfileName, fileType);
        errorExit(message);
    }
    
    //  if switches don't get assigned, exit
    nullCheck(switches);

    return switches;
}


//  returns pathname of temporary directory tarfile is extracted to
char  *extractTarfile(char *tarfile, char *topDir)
{
    int pid;
    int status;

    char *switches = getTarSwitches(tarfile, true);
    char *tempDir  = makeTempDir(topDir);

    switch (pid = fork()) {
    case -1:    forkError();

    case 0:     execlp("tar", "tar", switches, tarfile, "-C", tempDir, NULL);
                break;

    default:    wait(&status);
                tarCheck(status, topDir);
    }

    //  free allocated memory
    free(switches);

    return tempDir;
}


//  contents of inPath directory are archived with "tar" command
//  into filename outPath  
void createTarfile(char *inPath, char *outPath, char *topDir)
{
    int pid;
    int status;

    char *switches = getTarSwitches(outPath, false);

    switch (pid = fork()) {
    case -1:    forkError();

    case 0:     execlp("tar", "tar", switches, outPath, "-C", inPath, ".", NULL);
                break;

    default:    wait(&status);
                tarCheck(status, topDir);
    }

    //  free allocated memory
    free(switches);
}
