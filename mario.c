#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n; // var to get the height
    int z; // var to control how many dots
    do
    {
        n = get_int("Height: "); //input to the height
        z = n; // using 
    }
    while (n < 1 || n > 8); 
    for (int i = 0; i < n; i++)
    {
        for (int d = z - 1; d > 0; d--)  //prints the space. used the int z equals to n (height) so it will decresse the numbers of space each line 
        {
            printf(" ");
        }
        for (int j = -1; j < i; j++)
        {
            printf("#");
        }
        printf("\n");
        z--;
    }
}
