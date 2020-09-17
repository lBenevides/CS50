from sys import argv, exit
import csv

if len(argv) != 3: 
    print("write it right")
    exit(1)

database = open(argv[1], "r")  # open dna database using argv

reader = csv.reader(database)

header = next(reader)

file = open(argv[2], "r")

dna = next(file)


sequence = False  # using this boolean to suport the check sequence function

run = 1
longest_run = [1] * (len(header) - 1)  # created a list of the biggest STR sequences

for k in range(len(header) - 1):  # iterate loop, to check the sequences of each STR 

    for i in range(len(dna)):
        
        if dna[i:i + len(header[k + 1])] == header[k + 1]:  # if finds the SRT begings the loop
            
            j = i + len(header[k + 1])
            sequence = True
            
            while sequence == True:
                
                if dna[j:j + len(header[k + 1])] == header[k + 1]:  # the next element is a sequence? if yes, count and goes to the next
                    run += 1
                    j = j + len(header[k + 1])
                    
                    if run > longest_run[k]:
                        longest_run[k] = run
                else:                                               # if not, close this loop 
                    run = 1
                    sequence = False
                    break


count = 0
for row in reader:
    if int(row[1]) == longest_run[0]:
        
        for i in range(len(header) - 2):
            if int(row[i+2]) == longest_run[i+1]:
                count += 1
                
                if count == (len(header) - 2):
                    print(row[0])
                    exit(3)
            else:
                count = 0
                break
            
print("No Match")