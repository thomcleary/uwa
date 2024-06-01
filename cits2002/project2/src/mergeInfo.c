/*  CITS2002 Project 2 2020
    Name:               Thomas Cleary
    Student Number:     21704985
*/

#include "mergetars.h"


#define NON_INPUT_ARGS      2           //  argv[0] and argv[argc-1] are not input tarfiles
#define TMP_LOCATION        "/tmp"      //  set to path you want to create temporary directories/files in


//  returns a pointer to an initialised MERGE_INFO variable
MERGE_INFO *initMergeInfo(int argc, char *argv[]) 
{
    MERGE_INFO *mergeInfo = malloc(sizeof(*mergeInfo));
    nullCheck(mergeInfo);
    
    mergeInfo->numInTarfiles = argc - NON_INPUT_ARGS;
    
    mergeInfo->numExtracted = 0;

    //  will need to store numInTarfile path names
    mergeInfo->extractedTarPaths = calloc(mergeInfo->numInTarfiles, sizeof(*(mergeInfo->extractedTarPaths))); 
    nullCheck(mergeInfo->extractedTarPaths);

    mergeInfo->requestedOutPath  = strdup(argv[argc-1]);
    nullCheck(mergeInfo->requestedOutPath);

    //  tempParentPath = "TMP_LOCATION/NEW_TEMPLATE"    (NEW_TEMPLATE defined in fileHandling.c)
    mergeInfo->tempParentPath  = strdup(makeTempDir(TMP_LOCATION));
    nullCheck(mergeInfo->tempParentPath);

    //  tempOutPath    = "TMP_LOCATION/tempParentPath/NEW_TEMPLATE"
    mergeInfo->tempOutPath = strdup(makeTempDir(mergeInfo->tempParentPath));
    nullCheck(mergeInfo->tempOutPath);

    return mergeInfo;
}


//  frees allocated memory from a MERGE_INFO variable
void freeMergeInfo(MERGE_INFO *mergeInfo)
{
    //  free every char* in extractedTarPaths
    for (int i = 0; i < mergeInfo->numInTarfiles; i++) {
        free(mergeInfo->extractedTarPaths[i]);
    }
    free(mergeInfo->extractedTarPaths);
    free(mergeInfo->requestedOutPath);
    free(mergeInfo->tempParentPath);
    free(mergeInfo);
}
