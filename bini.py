ebrima = [['Gambia', 1992, 'March', 5], ['Oxford', 2010, 'April', 19], ['Lagos', 2015, 'January', 20], ['Stockholm', 2020, 'June', 1]]
# write a program that going to return the year I traveled to Lagos from the list above
# print(ebrima[2][1])

# user_input = input('Enter Year of travel: ')
# if user_input == 2015:
#     print(f'ebrima have travel to {ebrima:2}')


alieu = [9, 1, 25, 9, 18, 89, 0, 35]
# write a program that is going to change the ordering of the above list in decending order

# print(sorted(alieu, reverse=True))

# print(alieu.sort())
# Given the list, words, of strings below, filter out the palindromes and append to the initial empty list, pal

words = ['the', 'bib', 'mom', 'table', 'radar']
pal = []

def isPal(word):
    if word == word[::-1]:
        pal.append(word)


for word in words:
    isPal(word)

print(pal)




