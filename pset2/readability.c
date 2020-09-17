#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

// transform strings/char into ints(numbers) to simplify the count of letters/words/sentences
// maybe i can count the amount of words by the amount of spaces

float index(int Letters, int Words, int Sentences);

int main(void)
{
    string s = get_string("Text: ");
    int n = strlen(s); //lenght of the string
    float letters = 0;
    float words = 0;
    float sentences = 0;
    for (int i = 0; i < n; i++)
    {
        if (s[i + 1] == '\0') //check if the string is ending, so it will ad an space to count the last word
        {
            words++;
        }
        if (s[i] == ' ') //count spaces
        {
            words++;
        }
        else if (s[i] >= 'a' && s[i] <= 'z') //count the letters
        {
            letters++;
        }
        else if (s[i] >= 'A' && s[i] <= 'Z') //didnt figure out how to count capital letter in the same same 
        {
            letters++;
        }
        else if (s[i] == '.' || s[i] == '?' || s[i] == '!')
        {
            sentences++;
        }
    }


    float L = (letters * 100 / words); //indes
    float S = (sentences * 100 / words); //index

    //index = 0.0588 * L - 0.296 * S - 15.8

    float index = (0.0588 * L - 0.296 * S - 15.8); //index formula

    //printf("%.0f letters\n%.0f words\n%.0f sentences\n", letters, words, sentences);
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %.0f\n", index);
    }

}




