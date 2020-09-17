#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>

int main (void)
{
    FILE *novo = fopen("phone.csv", "r");
    FILE *test = fopen("test.csv", "w");

    unsigned int *buffer[20];
     fread(buffer,20, 1, novo);
        fwrite(buffer, 20, 1, test);
            
    
}
