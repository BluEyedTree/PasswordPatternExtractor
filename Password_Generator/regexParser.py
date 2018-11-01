import re


testRegex = "[a-z]{3}[0-9]{3}[a-z]{4}[0-9]{3}[a-z]{3}"

regexlList = []
for i in testRegex.split("{"):
    for j in i.split("}"):
        regexlList.append(j)

regexlList = regexlList[:-1]
print(regexlList)




formattedRegex = ""
for i in range(0,len(regexlList)-1,2):
    builtRegexToAdd = regexlList[i] + "{1}"
    formattedRegex += builtRegexToAdd*int(regexlList[i+1])

breakUpNumber = 0
count = 0
toAdd = []
#TODO: Write code to lump on the regex into char's of 3, and return that
'''
for i in formattedRegex.split("{1}"): #Get the items without the number

    if(breakUpNumber == breakUpNumber)

    count += 1
'''


print(formattedRegex.split("{1}"))

'''
class RegexParser():
    # Rocket simulates a rocket ship for a game,
    #  or a physics simulation.

    def __init__(self):
        # Each rocket has an (x,y) position.
        self.x = 0
        self.y = 0

    def move_up(self):
        # Increment the y-position of the rocket.
        self.y += 1
'''