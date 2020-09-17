from sys import argv, exit
import csv

if len(argv) != 3:
    print("write it right")
    exit(1)

database = open(argv[1], "r")

reader = csv.reader(database)

header = next(reader)

file = open(argv[2],"r")

dna = next(file)


sequence = False

run = 1
longest_run = [0] * (len(header) - 1)

for k in range(len(header) - 1):

    for i in range(len(dna)):
        if dna[i:i + len(header[k + 1])] == header[k + 1]:
            j = i + len(header[k + 1])
            sequence = True
            while sequence == True:
                if dna[j:j + len(header[k + 1])] == header[k + 1]:
                    run += 1
                    j = j + len(header[k + 1])
                    if run > longest_run[k]:
                        longest_run[k] = run
                else:
                    run = 1
                    sequence = False
                    break


check = False
count = 0
print(longest_run[0])
for row in reader:
    #print(int(row[1]))
    if int(row[1]) == longest_run[0]:
        
        for i in range(len(header) - 2):
            if int(row[i+2]) == longest_run[i+1]:
                count += 1
                
                if count == (len(header) - 2):
                    print(row[0])
            else:
                count = 0
                break
            
    