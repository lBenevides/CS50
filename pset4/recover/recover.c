#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>



int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return 1;
    }

    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        return 1;
    }

    unsigned char *buffer = malloc(512);
    int count = 0;
    int counter = 0;
    FILE *img;
    char *filename = malloc(10);
    while (fread(buffer, 1, 512, card) == 512)
    {
        if (buffer [0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (count == 0)
            {
                
                sprintf(filename, "%03i.jpg", count); 
                printf("File %i\n", count);
                img = fopen(filename, "w");
                fwrite(buffer, 1, 512, img);
                count++;
                counter++;
            }
            else if (count > 0)  
            {
                fclose(img);
              
                sprintf(filename, "%03i.jpg", count); 
                printf("File %i\n", count);
                
                img = fopen(filename, "w");
                fwrite(buffer, 1, 512, img);
                count++;
                counter++;
            }
        }
        else if (counter > 0) 
        {
            fwrite(buffer, 1, 512, img);
        }
    }
    fclose(card); 
    fclose(img);
    free(buffer);
    free(filename);
}
