import Password_Generator.regexParser as regexParser



def test_regexParser():
    regexTest1 = "[a-z]{2}[0-9]{1}"
    firstAnswer = ["[a-z]{1}[a-z]{1}", "[0-9]{1}"]

    regexTest2 = "[a-z]{2}[0-9]{2}"
    secondAnswer = ["[a-z]{1}[a-z]{1}", "[0-9]{1}[0-9]{1}"]
    print( regexParser.breakUPRegex(regexTest1,2))
    #a =  regexParser.regexParser.breakUPRegex(regexTest1,2)
#    regexParser.breakUPRegex("")
    assert  regexParser.breakUPRegex(regexTest1,2) == firstAnswer
    assert regexParser.breakUPRegex(regexTest2, 2) == secondAnswer



