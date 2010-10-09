#!/usr/bin/python

############################################
## Hangman 0.1.0 -- written by Max Dzyuba ##
############################################

# importing the needed functions

from random import choice
from re import match
import os

charlist = []
used_chars = []

inLetter = ''

#############
# TODO list #
###############################################################################
# Do you have a suggestion? Feel free to add a task here.
#
#
###############################################################################

#
# main functions
#

# get user input

def getChoice(menu):
    print menu
    choice = raw_input("Make your choice: ")
    choice = choice.lower()
    return choice

# clearing a history 

def clearing():
    global charlist, used_chars
    del charlist[:]
    del used_chars[:]

def init(categories, category):
    """
    Chooses a category, removes a used word, checks if the categories
    still have words in them.

    Type: Category list * Category -> unit
    """
    global tries, letters, wd
    def isEmpty(cat):
        return cat.isEmpty()
    if (all(map(isEmpty, categories))):
        print "\nNo category has any words left. The program will quit now."
        bye()
    elif (category.isEmpty()):
        print "\nThis category doesn't have more words. Try another category."
        starting()        
    else:
        wd      = category.getWord()
        tries   = len(wd)
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

# get user input in lower-case

def getLetter():
    global inLetter
    letter = raw_input('Enter your letter: ')
    inLetter = letter.lower()

# the main function -- handling user answers and communicating with him/her

def mainFunc(cats, cat):
    global tries, wd, letters, used_chars, charlist, inLetter
    init(cats,cat)
    print "The word has %d letters. You have %d chances to guess wrong. Enter the letter: " % (letters, letters),
    getLetter()

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
                else:
                    charlist.append(inLetter)
                    print "There is such letter in the word, congrats!"
                    print guessword
                    getLetter()
            else:
                print "Please enter one letter."
                getLetter()
        if inLetter not in wd:
            if (not match('.{2,}', inLetter)) and (match('[a-z]{1}', inLetter)):
                if inLetter in used_chars:
                    print "You already entered that letter. Try another one."
                    getLetter()
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
                        getLetter()
            else:
                print "Please enter one letter."
                getLetter()
        if (inLetter in wd) and (inLetter in charlist):
            if (not match('.{2,}', inLetter)) and (match('[a-z]{1}', inLetter)):
                print "You already entered that letter. Try another one."
                getLetter()
            else:
                print "Please enter one letter."
                getLetter()

class Category:
    """
    Represents a category of notions.
    """
    def __init__(self, name, words):
        self.name  = name
        self.words = words

    def isEmpty(self):
        """Tests if the category is empty."""
        return len(self.words) == 0

    def getWord(self):
        """
        Picks a new random word and removes it from the category.
        Type: unit -> string or None
        """
        if len(self.words) > 0:
            wd = choice(self.words)
            del self.words[self.words.index(wd)]
            return wd

def getCategories():
    """
    Discovers the categories from the data folder.
    Type: unit -> Category list
    """
    def nameCategory(cat):
        return cat.replace(".txt", "").replace("-"," ")
    def readCategory(path):
        f = open(path, 'r')
        r = map(lambda x: x.strip(), f.readlines())
        f.close()
        return r
    def getCategory(cat):
        return Category(nameCategory(cat), readCategory('data/' + cat))
    x = []
    for (d, ds, fs) in os.walk('data'):
        x = map(getCategory, fs)
    return x

def chooseCategory(categories):
    """
    Asks the user to choose a category. May exit the program.
    Type: Category list -> Category or None
    """
    print "    Choose a category (or quit)"
    print
    i = 0
    for x in categories:
        i = i + 1
        print "    (%i) %s" % (i, x.name)
    print
    print "    (q) Quit"
    choice = getChoice("")
    choose_from = range(len(categories)+1)
    del choose_from[0]
    for i in range(len(choose_from)):
        choose_from[i] = str(choose_from[i])
    print choose_from
    if choice in choose_from:
        n = int(choice) - 1
        if (n >= 0 and n < len(categories)):
            return categories[n]
    elif choice == 'q':
        bye()    
    else:
        starting()

def starting():
    """The entry-point of the program."""
    clearing()
    cats = getCategories()    
    cat  = None
    while cat == None:
        cat = chooseCategory(cats)
        if cat == None:
            print "\nEnter one of these: '1', '2', '3' or 'q'!\n"
    mainFunc(cats, cat)

if __name__ == "__main__":
    starting()
