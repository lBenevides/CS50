from cs50 import get_float

cash = 100 * get_float("Change owed: ")
while cash < 0:
    cash = 100 * get_float("Change owed: ")
    
# quarters (25¢), dimes (10¢), nickels (5¢), and pennies (1¢).

quarters = cash / 25 
dimes = (cash % 25) / 10
nickels = (cash % 25 % 10) / 5
pennies = (cash % 25 % 10 % 5)

change_count = int(quarters) + int(dimes) + int(nickels) + (pennies)  # sum all coins used

print(f"{int(change_count)}")  # print how many coins
