/*  CITS2002 Project 2 2020
    Name:               Thomas Cleary
    Student Number:     21704985
*/

#include "mergetars.h"


#define NEW_TEMPLATE    "mergetars.XXXXXX"


//  returns pointer to pathname of the created temporary directory
char *makeTempDir(char *path)
{
    char *template = calloc(MAXPATHLEN, sizeof(*template));
    nullCheck(template);

    pathLengthCheck(snprintf(template, MAXPATHLEN, "%s/%s", path, NEW_TEMPLATE), template);                                
    
    nullCheck(mkdtemp(template));

    return template;
}

//  makes new directory at path with mode permissions
//  checks if mkdir() fails
void makeDir(char *path, mode_t mode)
{
    nonZeroCheck(mkdir(path, mode));
}


//  copies binary contents of source into destination
//  sets access/modification time to times[0]/times[1]
//  sets file permissions to permissions
void copyFile(char *source, char *dest, struct timeval times[], mode_t permissions)
{
    FILE *fpIn  = fopen(source, "rb");
    nullCheck(fpIn);

    FILE *fpOut = fopen(dest,   "wb");
    nullCheck(fpOut);

    char    buffer[BUFSIZ];
    size_t  bytesRead, bytesWritten;

    while ((bytesRead = fread(buffer, 1, sizeof(buffer), fpIn)) > 0) {  
        
        bytesWritten = fwrite(buffer, 1, bytesRead, fpOut);
        
        //  did number of bytes read == number of bytes written?
        fReadWriteCheck(bytesWritten, bytesRead);
    }

    //  close the files
    nonZeroCheck(fclose(fpIn));
    nonZeroCheck(fclose(fpOut));
    
    //  set permissions and access/modification times
    nonZeroCheck(chmod(dest, permissions));
    nonZeroCheck(utimes(dest, times));
}


//  removes file/directory at path
//  checks if remove() fails
void removeFile(char *path)
{
    nonZeroCheck(remove(path));
}


//  returns true if path is not "." or ".."
//  else false
bool isValidFilename(char *path)
{
    if ((strcmp(path, ".") != 0) && (strcmp(path, "..") != 0)) {
        return true;
    }
    return false;
}


//  removes the directory dirPath
void removeDir(char *dirPath)
{
    char fullpath[MAXPATHLEN];

    DIR *dir = opendir(dirPath);
    nullCheck(dir);

    struct dirent   *dirEntry;

    //  for each file/directory in dir
    while ((dirEntry = readdir(dir)) != NULL) {  

        struct stat  *statBuffer = malloc(sizeof(*statBuffer));
        
        //  if the file is not "." or ".." 
        if (isValidFilename(dirEntry->d_name)) {

            pathLengthCheck(snprintf(fullpath, MAXPATHLEN, "%s/%s", dirPath, dirEntry->d_name), fullpath);

            nonZeroCheck(stat(fullpath, statBuffer));

            if (S_ISDIR(statBuffer->st_mode )) {
                removeDir(fullpath);
            }
            else if (S_ISREG(statBuffer->st_mode )) {
                removeFile(fullpath);
            }
        }
        //  free allocated memory
        free(statBuffer);
    }
    //  close the directory
    nonZeroCheck(closedir(dir));
    //  remove the directory
    removeFile(dirPath);
}
