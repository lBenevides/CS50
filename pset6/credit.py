from cs50 import get_int

card_number = get_int("Number: ")

card = card_number

count = 1
sum1 = 0
checksum = 0

c = card

while card_number >= 10:  # loop to know how many digits
    card_number /= 10
    count += 1

i = count/2

card = int(card * 10)

for x in range(int(i)+1):  # iterates the number, diving by 10 and add the sumcheck every division
    card = int(card/10)
    sum1 = sum1 + int((card % 10))
    card = int(card/10)
    sum1 = sum1 + int((((card % 10) * 2) / 10)) + int((((card % 10) * 2) % 10))


#  dictionary to find the values
cards = {
    34: "AMEX", 
    37: "AMEX",
    51: "MASTERCARD",
    52: "MASTERCARD",
    53: "MASTERCARD",
    54: "MASTERCARD",
    55: "MASTERCARD",
    4: "VISA"
}

#  first last digits to check the card brand
c = int(card_number * 10)

if c in cards:
    print(f"{cards[c]}")
elif int(c/10) in cards:  # as VISA is only for 4 not 4x
    print(f"{cards[int(c/10)]}")
else:
    print("INVALID")
