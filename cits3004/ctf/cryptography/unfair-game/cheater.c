#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define TOTAL_ROUNDS 100

int main() {
    // Set seed to current epoch time
    time_t seedTime = time(NULL);
    srand(seedTime);

    // Get enough random numbers to pass TOTAL_ROUNDS rounds
    int nums[TOTAL_ROUNDS];

    for (int i = 0; i < TOTAL_ROUNDS + 2; i++) {
        nums[i] = rand();
    }

    // write the numbers to a file
    FILE * fp;
    fp = fopen("nums.txt", "w+");

    for (int i = 0; i < TOTAL_ROUNDS + 2; i++) {
        fprintf(fp, "%d\n", nums[i]);
    }
    fclose(fp);
}

