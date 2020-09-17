import cs50
import sqlite3
from sys import argv, exit
import csv

if len(argv) != 2:
    print("write it right")
    exit(1)

chars = open(argv[1], "r")

# open database from SQLite3
conn = sqlite3.connect("students.db")
db = conn.cursor()

reader = csv.reader(chars)
header = next(reader)

first = None
middle = None
last = None

for row in reader:
    if row[0].count(" ") == 2: # indicates there are 3 names: name, middle and last
        name = row[0]
        name = name.split()

        first = name[0]
        middle = name[1]
        last = name[2]
    else:
        name = row[0]
        name = name.split()
        
        first = name[0]
        middle = None
        last = name[1]

    lista = [first, middle, last, row[1], row[2]] 
    db.executemany("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?);", [(first, middle, last, row[1], row[2])])    
    conn.commit()