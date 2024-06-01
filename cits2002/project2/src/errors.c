/*  CITS2002 Project 2 2020
    Name:               Thomas Cleary
    Student Number:     21704985
*/

#include "mergetars.h"

//  prints custom error message and usage information
//  then exits program with EXIT_FAILURE
void errorExit(char *message)
{
    printf("error: %s\n", message);
    inputHelp();
    exit(EXIT_FAILURE);
}


//  prints error message regarding number of command line inputs given
//  displays usage information
void argNumHelp(int argc) 
{
    printf("error: mergetars expected at least 2 arguments but recieved %i\n", argc);
    inputHelp();
}


// prints usage information for this program
void inputHelp(void)
{
    printf("usage: ./mergetars input_tarfile1 [input_tarfile2 ...] output_tarfile\n");
}


//  if the pointer, pointer, is NULL:
//      display error message and exit with EXIT_FAILURE
void nullCheck(void *pointer)
{
    if (pointer == NULL) {
        perror("error");
        exit(EXIT_FAILURE);
    }
}


//  if returned does not equal 0:
//      display error message and exit with EXIT_FAILURE
void nonZeroCheck(int returned)
{
    if (returned != 0) {
        perror("error");
        exit(EXIT_FAILURE);
    }
}


//  if returned is less than 0 (snprintf failure) 
//  or greater than the length of buffer (snprintf could not store all ouput in buffer):
//      print error message and exit with EXIT_FAILURE
void pathLengthCheck(int returned, char *buffer)
{
    if (returned < 0 || (returned > strlen(buffer))) {
        printf("error: path is longer than MAXPATHLEN\n");
        exit(EXIT_FAILURE);
    }
}


//  if strrchr returns a NULL pointer a file extension in filename was not found
//      print error message and usage information then exit with EXIT_FAILURE
void strrchrCheck(char *filename, char *remainingChars)
{
    if (remainingChars == NULL) {
        printf("error: %s has no file type specified\n", filename);
        inputHelp();
        exit(EXIT_FAILURE);
    }
}


//  if the number of bytes read to a file does not equal the amount read from the file:
//      print error message and exit with EXIT_FAILURE
void fReadWriteCheck(int wrote, int read)
{
    if (wrote != read) {
        printf("error: error copying files\n");
        exit(EXIT_FAILURE);
    }
}


//  if a fork() has failed, print error message and exit with EXIT_FAILURE
void forkError(void)
{
    perror("fork failed");
    exit(EXIT_FAILURE);
}


//  if a tar process returns a value other than 0, its execution failed
//  prints error message, removes temporary directories and exits with EXIT_FAILURE
void tarCheck(int returned, char *tempParentDir)
{
    if (returned != 0) {
        printf("error: tar encountered an error during execution\n");
        removeDir(tempParentDir);
        exit(EXIT_FAILURE);
    }
}
