from cs50 import get_int

# get int from the the user

height = get_int("Height: ") 
while height <= 0 or height > 8:  
    height = int(input("Height: "))
    
for i in range(height):
    for k in range(height - i - 1):  # print the spaces
        print(" ", end="")
    for j in range(i+1):   # print hashes
        print("#", end="")
    print(" ", end="")
    print(" ", end="")
    for j in range(i+1):   # print hashes again
        print("#", end="")
    print("\n", end="")  # news linesn

