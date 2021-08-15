/*
    Name: Wanuch Inthiravoranont
    BlazerId: wanuch
    Course Section: CS 432 or CS 632 or CS 732
    Homework #: 1
*/
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
double gettime(void){
  struct timeval tval;

  gettimeofday(&tval, NULL);

  return( (double)tval.tv_sec + (double)tval.tv_usec/1000000.0 );
}

int main(int argc, char **argv){
    int i, j, width, height, step, check, stop;
    int **old, **new;
    double starttime, endtime, value;

    /* Input sizes and generations of the game */
    int size = atoi(argv[1]);
    int generations = atoi(argv[2]);

    /* Random value in the game will not get the same value for each turn */
    srand(time(NULL));

    /* Allocate size and initial value */
    width  = size + 2;
    height = size + 2;

    old = malloc(width*sizeof(int*));
    new = malloc(width*sizeof(int*));

    for(i=0; i<width; i++){
        old[i] = malloc(height*sizeof(int));
        new[i] = malloc(height*sizeof(int));
    }

    /* Random value for each tuple in game of life */
    for (i=0; i<width; i++){
        for (j=0; j<height; j++){
            value = rand() / ((double)RAND_MAX);
            if(value < 0.5){
                old[i][j] = 0;
            }
            else {
                old[i][j] = 1;
            }
        }
    }

    /* Set zero for the bound */
    for(i=0; i<width; i++){
        for(j=0; j<height; j++){
            if(i == 0) old[i][j] = 0;
            else if(j == 0) old[i][j] = 0;
            else if(i == width-1) old[i][j] = 0;
            else if(j == height-1) old[i][j] = 0;
        }
    }

    /* Start stopwatch */
    starttime = gettime();

    /* Start play game of life */
    for(step=0; step<generations; step++){

        for(i=1; i<=size; i++){
            for(j=1; j<=size; j++){
                check = 0;

    /* Check cells surround the center cell */
                if(old[i-1][j-1] == 1) check++;
                if(old[i-1][j]   == 1) check++;
                if(old[i-1][j+1] == 1) check++;
                if(old[i][j-1]   == 1) check++;
                if(old[i][j+1]   == 1) check++;
                if(old[i+1][j-1] == 1) check++;
                if(old[i+1][j]   == 1) check++;
                if(old[i+1][j+1] == 1) check++;

    /* Set value for each cell by following
        1.  Each cell with one or no neighbor dies.
        2.  Each cell with four or more neighbors dies.
        3.  Each cell with two or three neighbors survives.
        4.  If a cell is “dead” in the current generation
            and there are exactly three neighbors "alive",
            then it will change to the "alive". */
               	if(check == 2) new[i][j] = old[i][j];
                else if(check == 3) new[i][j] = 1;
                else if(check < 2)  new[i][j] = 0;
                else if(check > 3)  new[i][j] = 0;
            }
        }
    /* 1. Check the life of game. If current board get the same tuple with
       the new board, then the program will stop.
       2. Move tuples from the new board to the current board. */
        stop =0;

        for(i=1; i<=size; i++){
            for(j=1; j<=size; j++){
                if(old[i][j] == new[i][j]){
                    stop++;
                }
                old[i][j] = new[i][j];
            }
        }

        /* Break the same generations */
        if(stop==(size*size)) break;
    }

    /* Stop stopwatch */
    endtime = gettime();

    /* Calculate stopwatch */
    printf("Time taken = %lf seconds\n", endtime-starttime);

    return 0;
}
