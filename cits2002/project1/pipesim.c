#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>


/*  CITS2002 Project 1 2020
    Name:                Thomas Cleary
    Student number(s):   21704985
*/


//  MAXIMUM NUMBER OF PROCESSES OUR SYSTEM SUPPORTS (PID=1..20)
#define MAX_PROCESSES                       20

//  MAXIMUM NUMBER OF SYSTEM-CALLS EVER MADE BY ANY PROCESS
#define MAX_SYSCALLS_PER_PROCESS            50

//  MAXIMUM NUMBER OF PIPES THAT ANY SINGLE PROCESS CAN HAVE OPEN (0..9)
#define MAX_PIPE_DESCRIPTORS_PER_PROCESS    10

//  TIME TAKEN TO SWITCH ANY PROCESS FROM ONE STATE TO ANOTHER
#define USECS_TO_CHANGE_PROCESS_STATE       5

//  TIME TAKEN TO TRANSFER ONE BYTE TO/FROM A PIPE
#define USECS_PER_BYTE_TRANSFERED           1


//  ---------------------------------------------------------------------------
//  YOUR DATA STRUCTURES, VARIABLES, AND FUNCTIONS SHOULD BE ADDED HERE:

//  LOOP PATTERN TO ITERATE OVER EVERY PROCESS 
//  [1, MAX_PROCESSES]
#define FOR_EACH_PROCESS        for(int process = 1; process <= MAX_PROCESSES; process++)

//  LOOP PATTERN TO ITERATE OVER EVERY PIPE DESCRIPTOR FOR A PROCESS
//  [0, MAX_PIPE_DESCRIPTORS_PER_PROCESS)
#define FOR_EACH_PIPE_DESC      for(int pipe = 0; pipe < MAX_PIPE_DESCRIPTORS_PER_PROCESS; pipe++)

//  LOOP PATTERN TO ITERATE OVER EVERY SYSTEM CALL MADE FOR A PROCESS
//  [0, MAX_SYS_CALLS_PER_PROCESS) 
#define FOR_EACH_SYS_CALL       for(int call = 0; call < MAX_SYSCALLS_PER_PROCESS; call++)

//  LENGTH OF THE READY QUEUE
#define QUEUE_SIZE              (MAX_PROCESSES+1)

//  ONE MICROSECOND
#define ONE_USEC                1

//  THE PROCESS THAT BOOTS INTO RUNNING
#define FIRST_PROCESS           1

//  VALUE TO REPRESENT NO PROCESS RUNNING ON CPU 
#define NO_PROCESS              0

//  THE STANDARD TERMINAL DISPLAY WIDTH
#define TERMINAL_WIDTH          80

//  EARLY DEFINITION TO ORDER FUNCTIONS NICELY
bool isValidPID(int pid);


//  ASSIGN VALUES TO POSSIBLE STATES A PROCESS CAN BE IN
enum { NEW=0,         READY,          RUNNING,           SLEEPING, 
       WAITING,       WRITEBLOCKED,   READBLOCKED,       EXITED };

//  ASSIGN VALUES TO INDIVIDUAL IMPLEMENTED SYSTEM CALLS
enum { SYS_COMPUTE=0, SYS_SLEEP,      SYS_EXIT,          SYS_FORK, 
       SYS_WAIT,      SYS_PIPE,       SYS_WRITEPIPE,     SYS_READPIPE };

int timetaken = 0;
int timeQuantum;
int pipeSize;

// CIRCULAR BLOCK QUEUE TO IMPLEMENT READY QUEUE OF PROCESS SCHEDULER
int readyQ[QUEUE_SIZE] = { 0 };
int head               = 0;
int tail               = QUEUE_SIZE - 1;

// STRUCTURE TO HOLD INFORMATION FOR EACH PROCESS IN A GIVEN EVENT FILE
struct process {
    int pid;
    int state;              //  NEW=0, READY=1, RUNNING=2,...
    int parent;             //  PID OF PARENT   
    int nextSysCall;        //  INDEX OF THE NEXT SYSTEM CALL TO PERFORM FROM sysCalls[]

    //
    struct pipe {
        bool using;         //  IS PROCESS USING THIS PIPE DESC?
        bool readOpen;      //  DOES THIS PIPE DESC HAVE A READER?
        bool isWriter;      //  IS THIS PROCESS THE WRITER OF THIS PIPE DESC?
        int  oppositePID;   //  PID OF PROCESS AT OTHER END OF PIPE, 0 IF NO PROCESS
        int  bytesInPipe;

    } pipes[MAX_PIPE_DESCRIPTORS_PER_PROCESS];  //  ARRAY OF ORDERED PIPES / DESCRIPTORS

    //
    struct systemCall {
        int  callType;        // SYS_COMPUTE=0, SYS_SLEEP=1,...
        int  usecs;          // sysCompute(), sysSleep()
        int  otherPID;       // sysFork(), sysWait()
        int  pipeDesc;       // sysPipe(), sysReadpipe(), sysWritepipe()
        int  numBytes;       // sysReadpipe(), sysWritepipe()

    } sysCalls[MAX_SYSCALLS_PER_PROCESS];       //  ARRAY OF ORDERED SYSTEM CALLS

} processes[MAX_PROCESSES + 1];                 //  +1 TO ALLIGN PIDs WITH THEIR INDEX IN THE ARRAY

//  POINTER TO CURRENT RUNNING PROCESS FROM processes[] 
struct process *running;


//  ---------------------------------------------------------------------------
//  DEBUGGING OUTPUT FUNCTIONS (NOT ESSENTIAL TO PROJECT REQUIREMENTS)

//  PRINT spaces NUMBER OF " "s
void printWhiteSpace(int spaces)
{
    for(int i = 0; i < spaces; i++) {
        printf(" ");
    }
}


//  PRINT numAsterisks NUMBER OF "*"s 
void printAsterisks(int numAsterisks)
{
    for(int i = 0; i < numAsterisks; i++) {
        printf("*");
    }
}


//  PRINT A DIVIDING LINE OF STANDARD TERMINAL WIDTH
void printWall(void)
{
    printf("\n");
    for(int dash = 0; dash < TERMINAL_WIDTH; dash++) {
        printf("-");
    }
    
    printf("\n\n");
}


//  PRINT THE CURRENT TIME TAKEN
void printTime(void)
{
    #define GAP     4

    printf("@%06i", timetaken);
    printWhiteSpace(GAP);

    #undef GAP
}


//  PRINT THE PID, pid
void printPID(int pid)
{
    printf("p%i: ", pid);
}


//  PRINT THE READY QUEUE
void printQueue(void)
{
    #define SPACING     1

    printf("RQ:");
    printWhiteSpace(SPACING);
    printf("[");

    int first = head;
    int printed = 0;

    while(readyQ[first] != NO_PROCESS && printed < MAX_PROCESSES) {
        if(first != head) {
            printf(",");
        }

        printWhiteSpace(SPACING);
        printf("%i", readyQ[first]);

        first = (first + 1) % QUEUE_SIZE;
        printed++;
    }

    printWhiteSpace(SPACING);
    printf("]\n");
}


//  PRINT A PROCESSES STATE CHANGE INFORMATION
void printStateChange(int pid, int nextState)
{
    printTime(); printPID(pid);

    switch (processes[pid].state) {
        case NEW:           printf("NEW---------->");
                            break;
        case READY:         printf("READY-------->");
                            break;
        case RUNNING:       printf("RUNNING------>");
                            break;
        case SLEEPING:      printf("SLEEPING----->");
                            break;
        case WAITING:       printf("WAITING------>");
                            break;
        case WRITEBLOCKED:  printf("WRITEBLOCKED->");
                            break;
        case READBLOCKED:   printf("READBLOCKED-->");
                            break;
    }
    switch (nextState) {
        case READY:         printf("READY..........");
                            break;
        case RUNNING:       printf("RUNNING\n");
                            break;
        case SLEEPING:      printf("SLEEPING\n");
                            break;
        case WAITING:       printf("WAITING\n");
                            break;
        case WRITEBLOCKED:  printf("WRITEBLOCKED\n");
                            break;
        case READBLOCKED:   printf("READBLOCKED\n");
                            break;
        case EXITED:        printf("EXITED\n");
                            break;
    }
}


//  PRINT SYS_COMPUTE CALL INFORMATION
void printComputeCall(int usecs)
{
    int  canCompute;
    bool completed;

    if(usecs > timeQuantum) {
        canCompute = timeQuantum;
        completed  = false;
    }
    else {
        canCompute = usecs;
        completed  = true;
    }

    printf("COMPUTE.......%i usecs", canCompute);

    if(completed) {
        printf(" (completed)\n");
    }
    else {
        printf(" (%i remaining)\n", usecs-timeQuantum);
    }
}


//  PRINT SYS_WRITEPIPE CALL INFORMATION
void printWritePipeCall(int numBytes, int inPipe, int pipeDesc, int readerPID)
{
    #define ALIGN_TUPLE     29

    int  canWrite     = pipeSize - inPipe;
    bool completed;

    if(numBytes > canWrite) {
        completed = false;
    }
    else {
        completed = true;
    }

    printf("WRITEPIPE.....(pipeDesc=%i, reader=", pipeDesc); 

    if(isValidPID(readerPID)) {
        printf("%i)\n", readerPID);
    }
    else {
        printf("NONE)");
    }

    printWhiteSpace(ALIGN_TUPLE);
    printf("(toWrite=%i, inPipe=%i)\n", numBytes, inPipe);
    printWhiteSpace(ALIGN_TUPLE);

    if(completed) {
        printf("(completed)\n");
    }
    else {
        printf("(written=%i, remaining=%i)\n", canWrite, numBytes-canWrite);
    }

    #undef ALIGN_TUPLE
}


//  PRINT SYS_READPIPE CALL INFORMATION
void printReadPipeCall(int numBytes, int inPipe, int pipeDesc, int writerPID)
{
    #define ALIGN_TUPLE     29

    bool completed;

    if(numBytes > inPipe) {
        completed = false;
    }
    else {
        completed = true;
    }

    printf("READPIPE......(pipeDesc=%i, writer=", pipeDesc); 

    if(isValidPID(writerPID)) {
        printf("%i)\n", writerPID);
    }
    else {
        printf("NONE)\n");
    }

    printWhiteSpace(ALIGN_TUPLE);
    printf("(toRead=%i, inPipe=%i)\n", numBytes, inPipe);
    printWhiteSpace(ALIGN_TUPLE);

    if(completed) {
        printf("(completed)\n");
    }
    else {
        printf("(read=%i, remaining=%i)\n", inPipe, numBytes-inPipe);
    }

    #undef ALIGN_TUPLE
}


//  PRINT INFORMATION FOR AN EXECUTED SYSTEM CALL
void printSysCall(int pid, int callType, struct systemCall *call)
{
    printTime(); printQueue();
    printWall();
    printTime(); printPID(pid);

    switch (callType) {
        case SYS_COMPUTE:       printComputeCall(call->usecs);
                                break;
        case SYS_SLEEP:         printf("SLEEP.........usecs=%i\n", call->usecs);
                                break;
        case SYS_FORK:          printf("FORK..........child=%i\n", call->otherPID);
                                break;
        case SYS_EXIT:          printf("EXIT\n");
                                break;
        case SYS_WAIT:          printf("WAIT..........on p%i\n", call->otherPID);
                                break;
        case SYS_PIPE:          printf("PIPE..........pipeDesc=%i\n", call->pipeDesc);
                                break;

        case SYS_WRITEPIPE: {   int  inPipe    = running->pipes[call->pipeDesc].bytesInPipe;
                                int  readerPID = running->pipes[call->pipeDesc].oppositePID;
                                printWritePipeCall(call->numBytes, inPipe, call->pipeDesc, readerPID);
                                break;
        }
        case SYS_READPIPE:  {   int  inPipe    = running->pipes[call->pipeDesc].bytesInPipe;
                                int  writerPID = running->pipes[call->pipeDesc].oppositePID;
                                printReadPipeCall(call->numBytes, inPipe, call->pipeDesc, writerPID);
                                break;
        }
    }

    printWall();
}


//  PRINT BLOCKED PROCESS STATE CHANGE INFORMATION
void printBlockedUpdate(char message[])
{
    #define GAP                 5
    #define FIRST_ASTERKISKS    10

    int messageLength      = strlen(message);
    int numSecondAsterisks = TERMINAL_WIDTH - (GAP * 2) - FIRST_ASTERKISKS - messageLength;

    printf("\n");

    printAsterisks(FIRST_ASTERKISKS); 
    printWhiteSpace(GAP); 
    printf("%s", message);
    printWhiteSpace(GAP);
    printAsterisks(numSecondAsterisks);
    
    printf("\n\n");

    #undef GAP
    #undef FIRST_ASTERKISKS
}


//  CREATES A WAITING FINISHED MESSAGE AND PRINTS IT
void printWaitFinished(int parentPID, int childPID)
{
    char message[] = "p%i HAS FINISHED WAITING FOR p%i";
    char messageCopy[sizeof(message)];

    snprintf(messageCopy, sizeof(messageCopy), message, parentPID, childPID);
    printBlockedUpdate(messageCopy);
}


// CREATES A READBLOCKED FINISHED MESSAGE AND PRINTS IT
void printReadBlockFinished(int pid, int pipeDesc)
{
    char message[] = "p%i CAN NOW READ FROM PIPE_DESC=%i";
    char messageCopy[sizeof(message)];

    snprintf(messageCopy, sizeof(messageCopy), message, pid, pipeDesc);
    printBlockedUpdate(messageCopy);
}


//  CREATES A WRITEBLOCKED FINISHED MESSAGE AND PRINTS IT
void printWriteBlockFinished(int pid, int pipeDesc)
{
    char message[] = "p%i CAN NOW WRITE TO PIPE_DESC=%i";
    char messageCopy[sizeof(message)];

    snprintf(messageCopy, sizeof(messageCopy), message, pid, pipeDesc);
    printBlockedUpdate(messageCopy);
}


//  CREATES A SLEEP FINISHED MESSAGE AND PRINTS IT
void printSleepFinished(int pid)
{
    char message[] = "p%i HAS FINISHED SLEEPING";
    char messageCopy[sizeof(message)];

    snprintf(messageCopy, sizeof(messageCopy), message, pid);
    printBlockedUpdate(messageCopy);
}


//  ---------------------------------------------------------------------------
//  DATA / DATA STRUCTURE FUNCTIONS

//  INITIALISE THE VALUES IN processes[] TO THEIR DEFAULT VALUES
void initProcesses(void)
{
    FOR_EACH_PROCESS {
        struct process *currProcess = &processes[process];

        currProcess->pid = process;

        if(process == 1) {
            currProcess->state = RUNNING;
        }
        else {
            currProcess->state = NEW;
        }

        currProcess->parent      = 0;
        currProcess->nextSysCall = 0;

        FOR_EACH_PIPE_DESC {
            struct pipe *currPipe = &currProcess->pipes[pipe];
            currPipe->using       = false;
            currPipe->readOpen    = false;
            currPipe->isWriter    = false;
            currPipe->oppositePID = 0;
            currPipe->bytesInPipe = 0;
        }

        FOR_EACH_SYS_CALL {
            struct systemCall *currCall = &currProcess->sysCalls[call];
            currCall->callType  = 0;
            currCall->usecs     = 0;
            currCall->otherPID  = 0;
            currCall->pipeDesc  = 0;
            currCall->numBytes  = 0;
        }
    }
}


//  SET nextSysCall FOR EVERY PROCESS IN processes[] TO 0, THE FIRST SYS_CALL
void resetNextSysCall(void)
{
    FOR_EACH_PROCESS {
        processes[process].nextSysCall = 0;
    }
}


//  RETURNS TRUE IF pid IS A VALID PID, ELSE FALSE
bool isValidPID(int pid)
{
    return pid > 0;
}


//  RETURNS TRUE IF readyQ IS EMPTY, ELSE FALSE
bool isQueueEmpty(void)
{   
    return head == (tail + 1) % QUEUE_SIZE;
}


//  isFull() NOT NECESSARY AS WE KNOW THERE CANNOT BE MORE THAN MAX_PROCESSES
//  EXISTING DURING SIMULATION
//  QUEUE_SIZE IS EQUAL TO MAX_PROCESSES SO WE WILL NEVER ATTEMPT TO ADD ONE
//  MORE TO A FULL QUEUE


//  ADDS pid TO THE END OF THE readYQ  
void enqueue(int pid)
{
    tail  = (tail + 1) % QUEUE_SIZE;
    readyQ[tail] = pid;
}


//  REMOVES THE HEAD OF THE readyQ AND RETURNS ITS' PID
int dequeue(void)
{
    int popped = readyQ[head];
    readyQ[head] = NO_PROCESS;
    head = (head + 1) % QUEUE_SIZE;

    return popped;
}


//  IF process IS SLEEPING, REMOVE usecs FROM ITS REMAINING SLEEP TIME
//  IF PROCESS HAS JUST MOVED TO SLEEPING (IS STILL running), DO NOT REMOVE usecs
//  (September 1st Project Clarification)
void updateSleepers(int usecs)
{
    FOR_EACH_PROCESS {
        struct process *currProcess = &processes[process];

        if(currProcess->state == SLEEPING && currProcess->pid != running->pid) {
            currProcess->sysCalls[currProcess->nextSysCall].usecs -= usecs;
        }
    }
}


//  INCREMENT timetaken BY usecs MICROSECONDS 
//  AND REMOVE usecs FROM SLEEPING PROCESSES
void progressTime(int usecs)
{
    timetaken += usecs;
    updateSleepers(usecs);

}


//  CHANGE THE STATE OF PROCESS pid FROM ITS CURRENT STATE TO nextState
void changeState(int pid, int nextState)
{
    printStateChange(pid, nextState);

    switch (nextState) {
        case READY:         enqueue(pid);
                            printQueue();
                            processes[pid].state = READY;
                            break;
        case RUNNING:       processes[pid].state = RUNNING;
                            running = &processes[pid];
                            break;
        case SLEEPING:      processes[pid].state = SLEEPING;
                            break;
        case WAITING:       processes[pid].state = WAITING;
                            break;
        case WRITEBLOCKED:  processes[pid].state = WRITEBLOCKED;
                            break;
        case READBLOCKED:   processes[pid].state = READBLOCKED;
                            break;
        case EXITED:        processes[pid].state = EXITED;
                            break;
    }

    // STATE CHANGE INCURS TIME COST
    progressTime(USECS_TO_CHANGE_PROCESS_STATE);
}


//  ---------------------------------------------------------------------------
//  PIPE MANAGEMENT FUNCTIONS

//  ASCOCIATE RUNNING PROCESSES' PIPES THAT HAVE NO READERS WITH PROCESS childPID
void assignParentPipes(int childPID)
{
    FOR_EACH_PIPE_DESC {
        if(running->pipes[pipe].readOpen) { //  PIPE HAS NO READER
            int bytesInPipe = running->pipes[pipe].bytesInPipe;

            processes[childPID].pipes[pipe].using        = true;
            processes[childPID].pipes[pipe].readOpen     = false;
            processes[childPID].pipes[pipe].isWriter     = false;
            processes[childPID].pipes[pipe].oppositePID  = running->pid;
            processes[childPID].pipes[pipe].bytesInPipe  = bytesInPipe;

            running->pipes[pipe].readOpen    = false;
            running->pipes[pipe].oppositePID = childPID;
        }
    }
}


//  CLOSE THE PIPES FOR THE CURRENT RUNNING PROCESS
void closePipes(void)
{
    FOR_EACH_PIPE_DESC {
        if(running->pipes[pipe].using) {
            // IF PROCESS IS WRITING END OF THIS pipe
            if(running->pipes[pipe].isWriter) {
                running->pipes[pipe].using       = false;
                running->pipes[pipe].isWriter    = false;
                running->pipes[pipe].bytesInPipe = 0;

                //  IF THERE IS ALSO A PROCESS READING FROM THIS pipe
                if(!running->pipes[pipe].readOpen) {
                    int readerPID = running->pipes[pipe].oppositePID;
                    processes[readerPID].pipes[pipe].oppositePID = 0;
                }

            }
            // IF PROCESS IS READING END OF THIS pipe
            else {
                running->pipes[pipe].using       = false;
                running->pipes[pipe].bytesInPipe = 0;
                int writerPID = running->pipes[pipe].oppositePID;

                //  IF THERE IS ALSO A PROCESS WRITING TO THIS pipe
                if(isValidPID(writerPID)) {
                    processes[writerPID].pipes[pipe].readOpen    = true;
                    processes[writerPID].pipes[pipe].oppositePID = 0;
                }
            }
        }
    }
}


// ----------------------------------------------------------------------------
// SYSTEM CALL FUNCTIONS


//  PROGRESS TIME BY THE THE REQUESTED COMPUTE TIME FROM call
//  UNLESS COMPUTE TIME > timeQuantum, THEN PROGRESS BY timeQuantum
//  AND SUBTRACT timeQuantum FROM usecs IN call
void sysCompute(struct systemCall *call)
{
    if(call->usecs <= timeQuantum) {
        progressTime(call->usecs);
        running->nextSysCall++; //  COMPUTED ALL usecs OF THIS call
    }
    else {
        progressTime(timeQuantum);
        call->usecs -= timeQuantum;
    }

    changeState(running->pid, READY);
}


//  CHANGE RUNNING PROCESS FROM RUNNING->SLEEPING
void sysSleep(struct systemCall *call)
{
    changeState(running->pid, SLEEPING);
}


//  CREATE A CHILD PID=call->otherPID FOR THE RUNNING PROCESS
//  MOVE CHILD TO readyQ
//  ASSIGN ANY OPEN PIPES TO THE CHILD
//  MOVE RUNNING PROCESS TO readyQ
void sysFork(struct systemCall *call)
{
    changeState(call->otherPID, READY);
    assignParentPipes(call->otherPID);

    processes[call->otherPID].parent = running->pid;

    changeState(running->pid, READY);
    running->nextSysCall++;
}


//  TERMINATE THE RUNNING PROCESS
//  CLOSE ALL ITS PIPE DESCRIPTORS
//  IF PARENT PROCESS IS WAITING FOR RUNNING PROCESS, CHANGE PARENT TO READY
void sysExit(struct systemCall *call)
{
    changeState(running->pid, EXITED);
    running->nextSysCall++; // IN CASE PID IS REUSED

    closePipes();

    int parentPID = running->parent;

    //  IF PROCESS HAS A PARENT (p1 DOES NOT)
    if(isValidPID(parentPID)) {
        struct process *parent = &processes[parentPID];

        if(parent->state == WAITING &&
           parent->sysCalls[parent->nextSysCall].otherPID == running->pid) {
                printWaitFinished(parentPID, running->pid);
                changeState(parentPID, READY);
                parent->nextSysCall++;
        }
    }
}


//  CHANGE RUNNING PROCESS FROM RUNNING->WAITING (ON call->otherPID)
void sysWait(struct systemCall *call)
{
    changeState(running->pid, WAITING);
}


//  MAKE THE RUNNING PROCESS THE WRITER OF call->pipeDesc 
void sysPipe(struct systemCall *call)
{
    running->pipes[call->pipeDesc].using    = true;
    running->pipes[call->pipeDesc].readOpen = true;
    running->pipes[call->pipeDesc].isWriter = true;

    changeState(running->pid, READY);
    running->nextSysCall++;
}


//  MAKES THE RUNNING PROCESS WRITE call->numBytes TO call->pipeDesc
//  IF MORE BYTES ARE REQUESTED THAN WHAT CAN FIT IN THE PIPE, RUNNING->WRITEBLOCKED
//  ELSE MOVE RUNNING->READY
void sysWritePipe(struct systemCall *call)
{
    int bytesInPipe   = running->pipes[call->pipeDesc].bytesInPipe;  //  BYTES IN PIPE
    int canWrite = pipeSize - bytesInPipe;                           //  SPACE IN PIPE
    int writeBytes;                                                  //  NUM BYTES TO WRITE

    if(call->numBytes > canWrite) {
        writeBytes = canWrite;
    }
    else {
        writeBytes = call->numBytes;
    }

    //  ADD BYTES TO PIPE
    running->pipes[call->pipeDesc].bytesInPipe += writeBytes;

    //  REMOVE BYTES FROM RUNNING PROCESSES' SYSTEM CALL
    call->numBytes -= writeBytes;

    progressTime(writeBytes * USECS_PER_BYTE_TRANSFERED);

    //  IF PROCESS STILL HAS BYTES LEFT TO WRITE
    if(call->numBytes > 0) {
        changeState(running->pid, WRITEBLOCKED);
    }
    else {
        changeState(running->pid, READY);
        running->nextSysCall++;
    }

    //  IF THIS PIPE HAS A READER, UPDATE READER
    if(!running->pipes[call->pipeDesc].readOpen) {
        int readerPID = running->pipes[call->pipeDesc].oppositePID;

        //  POINTER TO READER PROCESS
        struct process *reader = &processes[readerPID];

        //  ADD BYTES TO PIPE
        reader->pipes[call->pipeDesc].bytesInPipe += writeBytes;

        //  IF THE READER WAS READBLOCKED ON THIS PIPE, READBLOCKED->READY
        if(reader->state == READBLOCKED &&
           reader->sysCalls[reader->nextSysCall].pipeDesc == call->pipeDesc) {

            printReadBlockFinished(readerPID, call->pipeDesc);
            changeState(readerPID, READY);
        }
    }
}


//  MAKES THE RUNNING PROCESS READ call->numBytes TO call->pipeDesc
//  IF MORE BYTES ARE REQUESTED THAN WHAT CAN IS IN THE PIPE, RUNNING->READBLOCKED
//  ELSE MOVE RUNNING->READY
void sysReadPipe(struct systemCall *call)
{
    int bytesInPipe    = running->pipes[call->pipeDesc].bytesInPipe; //  BYTES IN PIPE
    int writerPID = running->pipes[call->pipeDesc].oppositePID;
    int readBytes;                                                  //  NUM BYTES TO READ

    if(call->numBytes > bytesInPipe) {
        readBytes = bytesInPipe;
    }
    else {
        readBytes = call->numBytes;
    }

    // REMOVE BYTES FROM PIPE
    running->pipes[call->pipeDesc].bytesInPipe -= readBytes;

    //  REMOVE BYTES FROM RUNNING PROCESSES' SYSTEM CALL
    call->numBytes -= readBytes;

    progressTime(readBytes * USECS_PER_BYTE_TRANSFERED);  

    // IF PROCESS STILL HAS BYTES LEFT TO READ
    if(call->numBytes > 0) {
        changeState(running->pid, READBLOCKED);
    }
    else {
        changeState(running->pid, READY);
        running->nextSysCall++;
    }

    // IF THIS PIPE HAS A WRITER, UPDATE WRITER
    if(isValidPID(writerPID)) {
        //  POINTER TO WRITER PROCESS
        struct process *writer = &processes[writerPID];

        //  REMOVE BYTES FROM PIPE
        writer->pipes[call->pipeDesc].bytesInPipe -= readBytes;

        //  IF THE WRITER WAS WRITEBLOCKED ON THIS PIPE, WRITEBLOCKED->READY
        if(writer->state == WRITEBLOCKED &&
           writer->sysCalls[writer->nextSysCall].pipeDesc == call->pipeDesc) {
               
            printWriteBlockFinished(writerPID, call->pipeDesc);
            changeState(writerPID, READY);
        }
    }
}


// EXECUTE THE RUNNING PROCESSES' NEXT SYSTEM CALL, call->callType
void runSystemCall(struct systemCall *call)
{
    printSysCall(running->pid, call->callType, call);

    switch (call->callType) {
        case SYS_COMPUTE:       sysCompute(call);
                                break;
        case SYS_SLEEP:         sysSleep(call);
                                break;
        case SYS_EXIT:          sysExit(call);
                                break;
        case SYS_FORK:          sysFork(call);
                                break;
        case SYS_WAIT:          sysWait(call);
                                break;
        case SYS_PIPE:          sysPipe(call);
                                break;
        case SYS_WRITEPIPE:     sysWritePipe(call);
                                break;
        case SYS_READPIPE:      sysReadPipe(call);
                                break;
    }
}


//  ---------------------------------------------------------------------------
//  RUN SIMULATION FUNCTIONS

//  CHECK TO SEE IF ANY PROCESSES THAT ARE SLEEPING ARE READY TO BE MOVED TO readyQ
void checkSleepers(void)
{
    FOR_EACH_PROCESS {
        struct process *currProcess = &processes[process];

        if(currProcess->state == SLEEPING) {
            if(currProcess->sysCalls[currProcess->nextSysCall].usecs <= 0) {
                printSleepFinished(currProcess->pid);
                changeState(currProcess->pid, READY);
                currProcess->nextSysCall++;
            }
        }
    }
}

//  RETURN TRUE IF THERE IS A PROCESS THAT EXISTS (process->state IS NOT NEW), THAT HAS NOT EXITED
//  ELSE RETURN FALSE
bool isProcessActive(void)
{
    FOR_EACH_PROCESS {
        int state = processes[process].state;

        if(state != EXITED && state != NEW) {
            return true;
        }
    }

    return false;
}


// RUN THE SIMULATION
void pipeSim(int tQuantum, int pSize)
{
    timeQuantum = tQuantum;
    pipeSize    = pSize;

    resetNextSysCall();

    // ASSIGN p1 TO RUNNING POINTER
    running = &processes[FIRST_PROCESS];

    printWall();
    printTime(); printf("p%i  BOOT--------->RUNNING\n", running->pid);

    //  POINTER TO RUNNING PROCESSES' FIRST SYSTEM CALL
    struct systemCall *firstSysCall = &running->sysCalls[running->nextSysCall];

    runSystemCall(firstSysCall);

    //  WHILE THERE IS AN ALIVE PROCESS
    while(isProcessActive()) {

        //  IF NO PROCESS IS READY TO EXECUTE ON CPU, PROGRESS TIME BY ONE USEC
        if(isQueueEmpty()) {
            running = &processes[NO_PROCESS];       //  THERE IS NO RUNNING PROCESS
            progressTime(ONE_USEC);
        }
        //  A PROCESS IS READY TO EXECUTE ON THE CPU
        else {
            changeState(dequeue(), RUNNING);    //  CHANGE STATE OF THE HEAD OF readyQ TO RUNNING

            //  POINTER TO RUNNING PROCESSES' NEXT SYSTEM CALL
            struct systemCall *nextSysCall = &running->sysCalls[running->nextSysCall];

            runSystemCall(nextSysCall);
        }

        //  CHECK SLEEPING PROCESSES BEFORE NEXT SYSTEM CALL
        checkSleepers();
    }

    //  NO MORE ALIVE PROCESSES

    printWall();
    printTime(); printf("HALT (no processes alive)\n");
    printWall();

    //  END SIMULATION
}


//  ---------------------------------------------------------------------------
//  FUNCTIONS TO VALIDATE FIELDS IN EACH eventfile - NO NEED TO MODIFY

int check_PID(char word[], int lc)
{
    int PID = atoi(word);

    if(PID <= 0 || PID > MAX_PROCESSES) {
        printf("invalid PID '%s', line %i\n", word, lc);
        exit(EXIT_FAILURE);
    }
    return PID;
}

int check_microseconds(char word[], int lc)
{
    int usecs = atoi(word);

    if(usecs <= 0) {
        printf("invalid microseconds '%s', line %i\n", word, lc);
        exit(EXIT_FAILURE);
    }
    return usecs;
}

int check_descriptor(char word[], int lc)
{
    int pd = atoi(word);

    if(pd < 0 || pd >= MAX_PIPE_DESCRIPTORS_PER_PROCESS) {
        printf("invalid pipe descriptor '%s', line %i\n", word, lc);
        exit(EXIT_FAILURE);
    }
    return pd;
}

int check_bytes(char word[], int lc)
{
    int nbytes = atoi(word);

    if(nbytes <= 0) {
        printf("invalid number of bytes '%s', line %i\n", word, lc);
        exit(EXIT_FAILURE);
    }
    return nbytes;
}

//  parse_eventfile() READS AND VALIDATES THE FILE'S CONTENTS
//  YOU NEED TO STORE ITS VALUES INTO YOUR OWN DATA-STRUCTURES AND VARIABLES
void parse_eventfile(char program[], char eventfile[])
{
#define LINELEN                 100
#define WORDLEN                 20
#define CHAR_COMMENT            '#'

//  ATTEMPT TO OPEN OUR EVENTFILE, REPORTING AN ERROR IF WE CAN'T
    FILE *fp    = fopen(eventfile, "r");

    if(fp == NULL) {
        printf("%s: unable to open '%s'\n", program, eventfile);
        exit(EXIT_FAILURE);
    }

    char    line[LINELEN], words[4][WORDLEN];
    int     lc = 0;

//  READ EACH LINE FROM THE EVENTFILE, UNTIL WE REACH THE END-OF-FILE
    while(fgets(line, sizeof line, fp) != NULL) {
        ++lc;

//  COMMENT LINES ARE SIMPLY SKIPPED
        if(line[0] == CHAR_COMMENT) {
            continue;
        }

//  ATTEMPT TO BREAK EACH LINE INTO A NUMBER OF WORDS, USING sscanf()
        int nwords = sscanf(line, "%19s %19s %19s %19s",
                                    words[0], words[1], words[2], words[3]);

//  WE WILL SIMPLY IGNORE ANY LINE WITHOUT ANY WORDS
        if(nwords <= 0) {
            continue;
        }

//  ENSURE THAT THIS LINE'S PID IS VALID
        int thisPID = check_PID(words[0], lc);

//  OTHER VALUES ON (SOME) LINES
        int otherPID, nbytes, usecs, pipedesc;

//  POINTER TO STRUCTURE TO STORE THE CURRENT LINE IN
        struct systemCall *currSysCall = &processes[thisPID].sysCalls[processes[thisPID].nextSysCall];

//  IDENTIFY LINES RECORDING SYSTEM-CALLS AND THEIR OTHER VALUES
//  THIS FUNCTION ONLY CHECKS INPUT;  YOU WILL NEED TO STORE THE VALUES
        if(nwords == 3 && strcmp(words[1], "compute") == 0) {
            usecs   = check_microseconds(words[2], lc);
            currSysCall->callType = SYS_COMPUTE;
            currSysCall->usecs    =   usecs;
        }
        else if(nwords == 3 && strcmp(words[1], "sleep") == 0) {
            usecs   = check_microseconds(words[2], lc);
            currSysCall->callType = SYS_SLEEP;
            currSysCall->usecs    =   usecs;
        }
        else if(nwords == 2 && strcmp(words[1], "exit") == 0) {
            currSysCall->callType = SYS_EXIT;
        }
        else if(nwords == 3 && strcmp(words[1], "fork") == 0) {
            otherPID = check_PID(words[2], lc);
            currSysCall->callType  = SYS_FORK;
            currSysCall->otherPID  = otherPID;
        }
        else if(nwords == 3 && strcmp(words[1], "wait") == 0) {
            otherPID = check_PID(words[2], lc);
            currSysCall->callType  = SYS_WAIT;
            currSysCall->otherPID  = otherPID;
        }
        else if(nwords == 3 && strcmp(words[1], "pipe") == 0) {
            pipedesc = check_descriptor(words[2], lc);
            currSysCall->callType  = SYS_PIPE;
            currSysCall->pipeDesc  = pipedesc;
        }
        else if(nwords == 4 && strcmp(words[1], "writepipe") == 0) {
            pipedesc = check_descriptor(words[2], lc);
            nbytes   = check_bytes(words[3], lc);
            currSysCall->callType  = SYS_WRITEPIPE;
            currSysCall->pipeDesc  = pipedesc;
            currSysCall->numBytes  = nbytes;
        }
        else if(nwords == 4 && strcmp(words[1], "readpipe") == 0) {
            pipedesc = check_descriptor(words[2], lc);
            nbytes   = check_bytes(words[3], lc);
            currSysCall->callType  = SYS_READPIPE;
            currSysCall->pipeDesc  = pipedesc;
            currSysCall->numBytes  = nbytes;
        }
//  UNRECOGNISED LINE
        else {
            printf("%s: line %i of '%s' is unrecognized\n", program,lc,eventfile);
            exit(EXIT_FAILURE);
        }
        processes[thisPID].nextSysCall++;
    }
    fclose(fp);

#undef  LINELEN
#undef  WORDLEN
#undef  CHAR_COMMENT
}


//  ---------------------------------------------------------------------------
//  CHECK THE COMMAND-LINE ARGUMENTS, CALL parse_eventfile(), RUN SIMULATION

int main(int argc, char *argv[])
{
    // IF INCORRECT NUMBER OF ARGUMENTS GIVEN
    if(argc != 4) {
        printf("%s expected 4 arguments, but recieved %i.\n", argv[0], argc);
        printf("Use: %s eventFile timeQuantum pipeSize\n", argv[0]);

        exit(EXIT_FAILURE);
    }
    else {
        int timeQuantum = atoi(argv[2]), pipeSize = atoi(argv[3]);

        //  SET EACH PROCESSES' DATA VALUES TO A DEFAULT
        initProcesses();

        // READ PROCESS DATA AND STORE IN PROCESS STRUCTURE WE JUST INITIALISED
        parse_eventfile(argv[0], argv[1]);

        // RUN THE SIMULATION
        pipeSim(timeQuantum, pipeSize);

        // PRINT TOTAL SIMULATION TIME IN MICROSECONDS
        printf("timetaken %i\n", timetaken);

        exit(EXIT_SUCCESS);
    }

    return 0;
}
