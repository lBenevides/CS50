#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>

// Ci = (Pi + k) % 26
// transform my string into 0 to 25 values then add k then convert to ASCII

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int x = strlen(argv[1]);
    for (int i = 0; i < x; i++)
    {
        if (isalpha(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int key = atoi(argv[1]);

    string plaintext = get_string("plaintext: "); //get the string

    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (isalpha(plaintext[i]))  //convert to alphet indx
        {
            if (islower(plaintext[i])) //small letters
            {
                plaintext[i] -= 97;
                plaintext[i] = (plaintext[i] + key) % 26 + 97;  //convert the number into alphabetic and then add 97 to convert back to ascii
            }
            else if (isupper(plaintext[i])) //capital letter
            {
                plaintext[i] -= 65;
                plaintext[i] = (plaintext[i] + key) % 26 + 65; //convert the number into alphabetic and then add 65 to convert back to ascii
            }
        }
    }
    printf("ciphertext: %s\n", plaintext);


}
