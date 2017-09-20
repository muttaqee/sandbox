'''
Created on Jan 26, 2017

This program applies a grammar to parse a string. It prints "Sender ok" if the
input string is in the form "MAIL FROM: <email>". Each function parses one rule
of the grammar. Start at the bottom of this file.

@author: muttaqee
'''

from sys import stdin
from sys import stdout

line = []         # Global variable for holding line of input
loc = 0           # Current location
errorFlag = False # Whether an error has been raised

a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXZ"
d = "0123456789"
special = "<>()[]\\.,;:@\"\n"

def parse():
    parseMailFromCmd()

def parseMailFromCmd():
    global loc

    if not accept("MAIL"):
        printError("mail from cmd")
        return False

    if not accept(" "):
        printError("mail from cmd")
        return False

    while accept(" "):
        continue

    if not accept("FROM:"):
        printError("mail from cmd")
        return False

    parseNullspace();

    if not parseReversePath():
        printError("reverse path")
        return False

    parseNullspace()

    if not parseCRLF():
        printError("CRLF")
        return False

    return True

def parseNullspace():
    while accept(" "):
        continue

def parseReversePath():
    return parsePath()

def parsePath():
    if not accept("<"):
        printError("path")
        return False

    if not parseMailbox():
        printError("mailbox")
        return False

    if not accept(">"):
        printError("path")
        return False

    return True

def parseMailbox():
    if not parseLocalPart():
        printError("local part")
        return False

    if not accept("@"):
        printError("mailbox")
        return False

    if not parseDomain():
        printError("domain")
        return False

    return True

def parseLocalPart():
    if not parseString():
        printError("local part")
        return False

    return True

def parseString():
    if not parseChar():
        return False

    while parseChar():
        continue

    return True

def parseChar():
    global line, loc, special
    if (line[loc] not in special) and line[loc] != " ":
        loc += 1
        return True
    else:
        return False

def parseDomain():
    if not parseElement():
        printError("domain")
        return False;
    elif accept("."):
        return parseDomain()
    else:
        return True

def parseElement():
    if not parseName():
        printError("name")
        return False

    return True

def parseName():
    if not parseA():
        printError("a")
        return False

    if not parseLetDigStr():
        printError("letter digit string")
        return False

    return True;

def parseA():
    global loc, a
    if line[loc] in a:
        loc += 1
        return True
    return False

def parseD():
    global loc, d

    if line[loc] in d:
        print("parsed d at " + str(loc) + ": " + line[loc])
        loc += 1
        return True

    return False

def parseLetDigStr():
    if not parseLetDig():
        printError("letter digit")
        return False

    while parseLetDig():
        continue

    return True

def parseLetDig():
    return parseA() or parseD()

def parseCRLF():
    if not accept("\n"):
        printError("CRLF")
        return False

    return True

def accept(string):
    global line, loc

    i = 0
    while i < len(string) and loc < len(line) and string[i] == line[loc]:
        i += 1
        loc += 1

    return i == len(string)

def printSuccess():
    print("Sender ok")

def printError(locationStr):
    global errorFlag

    if not errorFlag:
        print("ERROR -- " + locationStr)
        errorFlag = True

def run():
    global line, loc, errorFlag

    line = stdin.readline()
    loc = 0

    while line:
        stdout.write(line)
        if parseMailFromCmd():
            printSuccess()
        try:
            line = stdin.readline() # Next line
            loc = 0 # Reset location
            errorFlag = False # Reset flag
        except:
            printError("mail from cmd")
            break

    return

run()
exit()
