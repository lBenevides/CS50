#include "helpers.h"
#include <cs50.h>
#include <math.h>

typedef struct
{
    int rgbtRed;
    int rgbtGreen;
    int rgbtBlue;

}
original;


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)

    {
        for (int j = 0; j < width; j++)
        {
            int red = image[i][j].rgbtRed;  // store the variable red
            int blue = image[i][j].rgbtBlue; // store blue
            int green = image[i][j].rgbtGreen; //store green

            float avg = round((float)(red + blue + green) / 3); //sum all and divided by 3 to get de average

            image[i][j].rgbtRed = (int) avg; //turn back on int, to make sure there's no decimal number
            image[i][j].rgbtBlue = (int) avg;
            image[i][j].rgbtGreen = (int) avg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++) //dived by 2 so it'll only the half the path
        {
            int temp_red = image[i][width - 1 - j].rgbtRed;  //using temp var to store the variable to swap and line 111
            int temp_green = image[i][width - 1 - j].rgbtGreen;
            int temp_blue = image[i][width - 1 - j].rgbtBlue;

            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;

            image[i][width - 1 - j].rgbtRed = red;
            image[i][width - 1 - j].rgbtGreen = green;
            image[i][width - 1 - j].rgbtBlue = blue;

            image[i][j].rgbtRed = temp_red;
            image[i][j].rgbtGreen = temp_green;
            image[i][j].rgbtBlue = temp_blue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    original colors[height][width];


    for (int i = 0; i < height; i++) //create a backup of original values
    {
        for (int j = 0; j < width; j++)
        {
            colors[i][j].rgbtRed = image[i][j].rgbtRed;
            colors[i][j].rgbtGreen = image[i][j].rgbtGreen;
            colors[i][j].rgbtBlue = image[i][j].rgbtBlue;
        }
    }

    for (int i = 0; i < height; i++) //iterate height columns
    {
        for (int j = 0; j < width; j++) //iterate width columns
        {
            float avg = 0.0;  //put here to reset every time the loop goes back

            float red_total = 0;
            float green_total = 0;
            float blue_total = 0;

            int up = 0;
            int down = 0;
            int left = 0;
            int right = 0;

            if (i - 1 >= 0)
            {
                up = 1;
            }
            if (i + 1 < height)
            {
                down = 1;
            }
            if (j - 1 >= 0)
            {
                left = 1;
            }
            if (j + 1 < width)
            {
                right = 1;
            }

            for (int h = i - up; h <= i + down; h++)
            {
                for (int w = j - left; w <= j + right; w++)
                {
                    red_total += colors[h][w].rgbtRed;
                    green_total += colors[h][w].rgbtGreen;
                    blue_total += colors[h][w].rgbtBlue;

                    avg++;
                }

            }

            image[i][j].rgbtRed = round((float) red_total / avg);  //sum all reds and divde by the amount of squares
            image[i][j].rgbtGreen = round((float) green_total / avg);
            image[i][j].rgbtBlue = round((float) blue_total / avg);

        }

    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    //creating Gx array
    int Gx[3][3] =
    {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };
    //creating Gy array
    int Gy[3][3] =
    {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1}
    };

    for (int i = 0; i < height; i++) //adding the pixels to a copy of the original image so i can use the copy to add values
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j].rgbtRed = image[i][j].rgbtRed;
            copy[i][j].rgbtGreen = image[i][j].rgbtGreen;
            copy[i][j].rgbtBlue = image[i][j].rgbtBlue;
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++) // treat pixels beyond corner as pure black (value 0)
        {
            int up = 0;
            int down = 0;
            int left = 0;
            int right = 0;
            
            int hp = 1; //using this var to multiplicate values in array Gx
            int wp = 1; //using this var to multiplacte values in array Gy

            long gx_red = 0; 
            long gy_red = 0;
            long gx_green = 0;
            long gy_green = 0;
            long gx_blue = 0;
            long gy_blue = 0;

            if (i - 1 >= 0) //check if's a corner
            {
                up = 1;
            }
            if (i + 1 < height) //check if's a corner
            {
                down = 1;
            }
            if (j - 1 >= 0) //check if's a corner
            {
                left = 1;
            }
            if (j + 1 < width) //check if's a corner
            {
                right = 1;
            }

            for (int h = i - up; h <= i + down; h++, hp++)
            {
                for (int w = j - left; w <= j + right; w++, wp++)
                {
                    gx_red += copy[h][w].rgbtRed * Gx[hp - up][wp - left];
                    gy_red += copy[h][w].rgbtRed * Gy[hp - up][wp - left];

                    gx_green += copy[h][w].rgbtGreen * Gx[hp - up][wp - left];
                    gy_green += copy[h][w].rgbtGreen * Gy[hp - up][wp - left];

                    gx_blue += copy[h][w].rgbtBlue * Gx[hp - up][wp - left];
                    gy_blue += copy[h][w].rgbtBlue * Gy[hp - up][wp - left];

                }
                wp = 1; //setting that back to 1 cause the loop will repeat more tem 3 times and wp would get bigger than the array
                
            }

            if (sqrt(gx_red * gx_red + gy_red * gy_red) > 255) //check if's bigger than 255
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = round(sqrt(gx_red * gx_red + gy_red * gy_red));
            }
            if (sqrt(gx_green * gx_green + gy_green * gy_green) > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = round(sqrt(gx_green * gx_green + gy_green * gy_green));
            }
            if (sqrt(gx_blue * gx_blue + gy_blue * gy_blue) > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = round(sqrt(gx_blue * gx_blue + gy_blue * gy_blue));
            }

        }

    }

    return;
}
