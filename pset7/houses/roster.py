import csv
import cs50
from sys import argv

if len(argv) != 2:
    print("write it right")
    exit(1)

houses = argv[1]

db = cs50.SQL("sqlite:///students.db")

for i in db.execute("SELECT first, middle, last, house, birth FROM students WHERE house = ? ORDER BY last, first", houses):
    print(i['first'], end=" ")
    if i['middle'] != None:
        print(i['middle'], end=" ")
    print(i['last'], end=", ")
    print("born", end=" ")
    print(i['birth'])


