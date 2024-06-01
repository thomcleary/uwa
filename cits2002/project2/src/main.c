/*  CITS2002 Project 2 2020
    Name:               Thomas Cleary
    Student Number:     21704985
*/

#include "mergetars.h"

//  command line arguments are assumed to be correct (from project spec)
int main(int argc, char *argv[]) {
    
    // if atleast 1 input tarfile and an output tarfile name are not provided
    if ((argc - 1) < 2) {
        argNumHelp(argc - 1);
        exit(EXIT_FAILURE);
    }
    else {
        mergetars(argc, argv);
        exit(EXIT_SUCCESS);
    }
    
    return 0;
}
