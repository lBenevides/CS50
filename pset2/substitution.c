#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>


int main(int argc, string argv[])
{
    //inputs
    if (argc != 2) //confirms if something's written after command
    {
        printf("Usage: ./substitution key.\n");
        return 1;
    }
    int length = strlen(argv[1]); //confirm if it's 26 letters
    if (length != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    for (int i = 0; i < length; i++)
    {
        if (isdigit(argv[1][i])) //confirm if is digits
        {
            printf("Key must contain only alphabetic characters.\n");
            return 1;
        }
        char z = argv[1][i];
        for (int y = i + 1; y < length; y++) //confirm is has duplicates
        {
            if (z == argv[1][y])
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }

//calculus of the cipher
// need a loop to identify each char and assemble then as the other
    string plain = get_string("plaintext: "); //input
    printf("ciphertext: "); //output
    for (int i = 0, n = strlen(plain); i < n; i++)
    {
        if (isalpha(plain[i])) //letter?
        {
            if (isupper(plain[i])) //is uppercase?
            {
                int cipher = plain[i] - 65;
                char c = argv[1][cipher];
                if (islower(c))         //confirm is the key is lower case
                {
                    c = c - 32;
                }
                printf("%c", c);  //prints the input of key

            }
            else if (islower(plain[i]))
            {
                //(key letter - letter) + 97
                int cipher = plain[i] - 97;
                char c = argv[1][cipher];
                if (isupper(c))
                {
                    c = c + 32;
                }
                printf("%c", c);
            }
        }
        else
        {
            printf("%c", plain[i]);
        }
    }
    printf("\n"); //new line
}