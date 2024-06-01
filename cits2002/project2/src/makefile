PROJECT = mergetars
HEADERS = $(PROJECT).h 
OBJ     = main.o mergetars.o errors.o mergeInfo.o fileHandling.o tarfileHandling.o addFiles.o

C99     = cc -std=c99 
CFLAGS  = -Wall -pedantic -Werror

$(PROJECT) : $(OBJ)
	$(C99) $(CFLAGS) -o $(PROJECT) $(OBJ)

%.o : %.c $(HEADERS)
	$(C99) $(CFLAGS) -c $<

clean:
	rm -f $(PROJECT) $(OBJ)

