# index = 0.0588 * L - 0.296 * S - 15.8
# L is the average number of letters per 100 words in the text
# and S is the average number of sentences per 100 words in the text.

from cs50 import get_string

text = get_string("Text: ")

letters = 0

for i in range(len(text)):
    if text[i].isalpha():
        letters += 1

words = text.count(" ") + 1

sentences = text.count(".") + text.count("?") + text.count("!")

# letters = len(text) - words - sentences

index = 0.0588 * (letters * 100 / (words)) - 0.296 * (sentences * 100 / (words)) - 15.8

if index >= 16:
    print("Grade 16+")
elif index < 1:
    print("Before Grade 1")
else:
    print(f"Grade {round(index)}")
    