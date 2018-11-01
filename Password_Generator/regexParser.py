


testRegex = "[a-z]{3}[0-9]{3}[a-z]{4}[0-9]{3}[a-z]{3}"

regexlList = []
for i in testRegex.split("{"):
    for j in i.split("}"):
        regexlList.append(j)

regexlList = regexlList[:-1]
print(regexlList)


for i in range(0,len(regexlList)-1,2):
    builtRegexToAdd = regexlList[i] + "{1}"
    print(builtRegexToAdd*int(regexlList[i+1]))




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