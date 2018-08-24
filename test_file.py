import Main
import DiskDic
import shelve
import os

'''
def test_substring_one_char():
    assert Main.subStringFinder("c") == {"c"}


def test_substring_two_char():
    assert Main.subStringFinder("ca") == {"c","a","ca"}
'''

def test_diskDic_adding_element():
    #Create the DB, then add elements, then delete what you created
    os.remove("testDB.db")
    with shelve.open('testDB', 'c') as shelf:
        pass

    diskdic = DiskDic.DiskDic("testDB")
    diskdic.add("Hello")
    diskdic.add("Hello")

    helloCount = 0
    with shelve.open('testDB', 'r') as shelf:
        helloCount = shelf["Hello"]
    assert helloCount == 2

