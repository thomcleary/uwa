/*  CITS2002 Project 2 2020
    Name:               Thomas Cleary
    Student Number:     21704985
*/

#include "mergetars.h"


//  copies files/directories from extractPath to outPath if they meet the selection criteria
void addFiles(char *extractPath, char *outPath)
{
    char extractFullPath[MAXPATHLEN];
    char outFullPath[MAXPATHLEN];

    //  struct to store file/directory access/modification
    //  tv_usec not needed, so set to 0
    struct timeval times[2];
    times[0].tv_usec = 0;
    times[1].tv_usec = 0;

    DIR *dir = opendir(extractPath);
    nullCheck(dir);

    struct dirent *dirEntry;

    // for each file/directory in dir
    while((dirEntry = readdir(dir)) != NULL) { 

        struct stat  *extractStats = malloc(sizeof(*extractStats));
        nullCheck(extractStats);

        struct stat  *outStats     = malloc(sizeof(*outStats));
        nullCheck(outStats);

        //  if file is not "../" or "./"
        if (isValidFilename(dirEntry->d_name)) {

            pathLengthCheck(snprintf(extractFullPath, MAXPATHLEN, "%s/%s", extractPath, dirEntry->d_name),
                            extractFullPath);
                            
            pathLengthCheck(snprintf(outFullPath, MAXPATHLEN, "%s/%s", outPath, dirEntry->d_name),
                            extractFullPath);

            nonZeroCheck(stat(extractFullPath, extractStats));

            //  set access/modification times to the same as file in extractFullPath
            times[0].tv_sec = extractStats->st_atime;
            times[1].tv_sec = extractStats->st_mtime;

            if (S_ISDIR(extractStats->st_mode)) {
                //  if the directory does not exist in the temporary output, make it
                if (stat(outFullPath, outStats) != 0) {
                    makeDir(outFullPath, extractStats->st_mode);
                }
                //  if directory exists in the temporary output and its modification time is more recent 
                //  set atime and mtime to this directories times
                else if (extractStats->st_mtime < outStats->st_mtime) {
                    times[0].tv_sec = outStats->st_atime;
                    times[1].tv_sec = outStats->st_mtime;
                }

                //  traverse this directory (depth first search)
                addFiles(extractFullPath, outFullPath);

                //  once traversed, set atime and mtime to times[0] and times[1]
                nonZeroCheck(utimes(outFullPath, times));
            }

            else if (S_ISREG(extractStats->st_mode)) {

                bool outFileExists = !stat(outFullPath, outStats);

                if (!outFileExists) {
                    copyFile(extractFullPath, outFullPath, times, extractStats->st_mode);
                }

                bool extractTimeGreater        = extractStats->st_mtime  > outStats->st_mtime;
                bool extractTimeEqual          = extractStats->st_mtime == outStats->st_mtime;
                bool extractSizeGreaterOrEqual = extractStats->st_size  >= outStats->st_size;

                if (outFileExists &&
                    (extractTimeGreater || (extractTimeEqual  && extractSizeGreaterOrEqual))) {
                    
                    removeFile(outFullPath);
                    copyFile(extractFullPath, outFullPath, times, extractStats->st_mode);

                    //  if extractTime == outTime and extractSize == outSize:
                    //      still copy extractFullPath
                    //  the order we extract the input tarfiles is the same as the order in which
                    //  they are specified on the command line. 
                    //  So this will always add the most recently specified (on the command line)
                }
            }
        }
        //  free allocated memory
        free(extractStats);
        free(outStats);
    }
    nonZeroCheck(closedir(dir));
}
