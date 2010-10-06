#!/usr/bin/python

############################################
## Hangman 0.1.0 -- written by Max Dzyuba ##
############################################

# importing the needed functions

from random import choice
from re import match

def readFile(path):
    f = open(path, 'r')
    r = map(lambda x: x.strip(), f.readlines())
    f.close()
    return r

# lists of words

animals = readFile("data/animals.txt")
body    = readFile("data/body-parts.txt")
fruits  = readFile("data/fruit.txt")

charlist = []
used_chars = []

#############
# TODO list #
###############################################################################
# provide support for custom lists (text file with words in a special format) #
###############################################################################

#
# main functions
#

# get user input

def getChoice(menu):
    print menu
    choice = raw_input("Make your choice: ")
    print bool(choice)
    return choice

# clearing a history 

def clearing():
    global charlist, used_chars
    del charlist[:]
    del used_chars[:]

# choosing a category, removing a used word, checking if the categories still have words in them

def init(cat):
    global tries, letters, wd, animals, body, fruits
    if ((len(animals) < 1) and (len(body) < 1) and (len(fruits) < 1)):
        print "\nNo category has any words left. The program will quit now."
        bye()
    if cat == 1:
        if len(animals) >= 1:
            wd = choice(animals)
            del animals[animals.index(wd)]
        else:
            print "\nThis category doesn't have more words. Try another category."
            starting()
    elif cat == 2:
        if len(body) >= 1:
            wd = choice(body)
            del body[body.index(wd)]
        else:
            print "\nThis category doesn't have more words. Try another category."
            starting()
    elif cat == 3:
        if len(fruits) >= 1:
            wd = choice(fruits)
            del fruits[fruits.index(wd)]
        else:
            print "\nThis category doesn't have more words. Try another category."
            starting()
    tries = len(wd)
    letters = len(wd)    

def bye():
    print "\nBye! Play again soon.\n"
    raise SystemExit

# masking the letters of the word to guess

def stars(word,char):
    global charlist, wd
    newWord = wd[:]
    for i in range(len(newWord)):
        if ((char != newWord[i]) and (newWord[i] not in charlist)):
                newWord = newWord.replace(newWord[i],'*')
    return newWord

# the main function -- handling user answers and communicating with him/her

def mainFunc(cat):
    global tries, wd, letters, used_chars, charlist
    init(cat)
    print "The word has %d letters. You have %d chances to guess wrong. Enter the letter: " % (letters, letters),
    inLetter = raw_input()

    while (tries != 0):
        if (inLetter in wd) and (inLetter not in charlist):
            if (not match('.{2,}', inLetter)) and (match('[a-z]{1}', inLetter)):
                guessword = stars(wd,inLetter)
                if (guessword == wd):
                    print "The word was:"
                    print "\n%s" % guessword
                    print """
=================
|    You won!   |
================="""
                    starting()
#                    break # testing...
                else:
                    charlist.append(inLetter)
                    print "There is such letter in the word, congrats!"
                    print guessword
                    inLetter = raw_input('Enter your letter: ')
            else:
                print "Please enter only one lower-case letter!"
                inLetter = raw_input('Enter your letter: ')
        if inLetter not in wd:
            if (not match('.{2,}', inLetter)) and (match('[a-z]{1}', inLetter)):
                if inLetter in used_chars:
                    print "You already entered that letter. Try another one."
                    inLetter = raw_input('Enter your letter: ')
                else:
                    tries -= 1
                    if (tries == 0):
                        print """
): You lost. Try again if you want :("""
                        print "\nThe word was '%s'" % wd
                        starting()
                    else:
                        print "Wrong! %d chances left." % tries
                        used_chars.append(inLetter)
                        inLetter = raw_input('Enter your letter: ')
            else:
                print "Please enter only one lower-case letter!"
                inLetter = raw_input('Enter your letter: ')
        if (inLetter in wd) and (inLetter in charlist):
            if (not match('.{2,}', inLetter)) and (match('[a-z]{1}', inLetter)):
                print "You already entered that letter. Try another one."
                inLetter = raw_input('Enter your letter: ')
            else:
                print "Please enter only one lower-case letter!"
                inLetter = raw_input('Enter your letter: ')

# the entrance function, numeric menu

def starting():
    clearing()
    menu = '''
    Choose a category (or quit):

    (1) Animals
    (2) Body parts
    (3) Fruits

    (q) Quit
    '''

    choice = getChoice(menu)
    if not (choice == ''):
        while (choice):
            if (choice == '1'):
                mainFunc(1)
            elif (choice == '2'):
                mainFunc(2)
            elif (choice == '3'):
                mainFunc(3)
            elif (choice == 'q'):
                bye()
            else:
                print "\nEnter one of these: '1', '2', '3' or 'q'!\n"
                choice = getChoice(menu)
    else:
        starting()

if __name__ == "__main__":
    starting()
