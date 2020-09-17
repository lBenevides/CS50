// Implements a dictionary's functionality

#include <stdbool.h>

#include "dictionary.h"
#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 676;

// Hash table
node *table[N];

//global variable for word count
unsigned int word_count;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //iterating each word at the given location using hash function to compare if the word is in the dictionary
    for (node *counter = table[hash(word)]; counter != NULL; counter = counter -> next)
    {
        int result = strcasecmp(word, counter -> word);
        if (result == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int num1 = 0;
    int num2 = 0;
    
    //this is a simple hash function. It just takes the 2 first words and index them into numbers so AA is 0, AB is 1...
    
    if (isalpha(word[0]))
    {
        if(isupper(word[0]))
        {
            num1 = (word[0] - 65) * 26;
        }
        else
        {
            num1 = (word[0] -97) * 26;
        }
    }
    if (isalpha(word[1]))
    {
        if(isupper(word[1]))
        {
            num2 = word[1] - 65;
        }
        else
        {
            num2 = word[1] - 97;
        }
    }
    return (num1 + num2);
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //open the file 
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Couldn't open the file\n");
        return false;
    }

    char names[LENGTH+1];

    node *n = NULL;
    //scan each word and put them on a linked list using a hash function to know the right index of the array;
    while (fscanf(file, "%s", names) != EOF )
    {
        n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n -> word, names);
        n -> next = table[hash(names)];
        table[hash(names)] = n;
        word_count++;

    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    //make sure that read all the words in the dictionary
    unsigned int free_count = 0;
    
    node *tmp = NULL;
    
    //iterate each index of the array to clean the linked list in it
    for (int i = 0; i < N; i++)
    {
        for(node *cursor = table[i]; cursor != NULL; )
        {
            tmp = cursor; //points to the cursor
            cursor = cursor ->next; //moves the curser to the other node
            free(tmp); 
            free_count++; 
        }

    }
    if (free_count == size())
    {
        return true;
    }


       // TODO
    return false;
}
