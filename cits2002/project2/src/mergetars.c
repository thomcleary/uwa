/*  CITS2002 Project 2 2020
    Name:               Thomas Cleary
    Student Number:     21704985
*/

#include "mergetars.h"


//  "merges" contents of argv[1] - argc[argc-2] into argv[argc-1]
void mergetars(int argc, char *argv[])
{
    //  allocate memory for storing file path information
    MERGE_INFO *mergeInfo = initMergeInfo(argc, argv);

    char **extractedTarPaths = mergeInfo->extractedTarPaths;

    //  for each input tarfile:
    //      - extract it into a temporary directory
    //      - store the temporary directory's file path
    for (int i = 1; i <= mergeInfo->numInTarfiles; i++)
    {
        extractedTarPaths[mergeInfo->numExtracted] = strdup(extractTarfile(argv[i], mergeInfo->tempParentPath));
        nullCheck(extractedTarPaths[mergeInfo->numExtracted]);
        mergeInfo->numExtracted++;
    }

    //  for each extracted tarfile:
    //      - add its files/directories to the temporary "out" directory
    //        (if they meet the selection criteria)
    for (int i = 0; i < mergeInfo->numExtracted; i++) {
        addFiles(extractedTarPaths[i], mergeInfo->tempOutPath);
    }

    //  tar the temporary "out" directory into the requested "out" tarfile
    createTarfile(mergeInfo->tempOutPath, mergeInfo->requestedOutPath, mergeInfo->tempParentPath);

    //  remove all temporary files/directories
    removeDir(mergeInfo->tempParentPath);

    //  free allocated memory
    freeMergeInfo(mergeInfo);
}
