import json
import time

"""Implementation of a retriveal tree."""

class Trie:

    def __init__(self):
        self.root = Node()

    """Inserts a single word into the tree. If the word already exists it will not be
       inserted more than once."""
    def insert(self, word):

        if word == "":
            return

        childs = self.root.children
        lastNode = None
        for letter in word:
            newNode = None
            if letter in childs:
                newNode = childs[letter]
            else:
                newNode = Node()
                childs[letter] = newNode
            childs = newNode.children
            lastNode = newNode
        lastNode.endOfWord = True

    """Finds the given word in the trie. Only searches for whole words. Return true of false based on existance."""
    def find(self, word):
        currentNodeChildren = self.root.children
        for letter in word:
            try:
                if currentNodeChildren[letter] is not None:
                    if currentNodeChildren[letter].endOfWord == True:
                        return True
                    currentNodeChildren = currentNodeChildren[letter].children
            except KeyError:
                return False

    """Inserts multiple words into trie."""
    def insert_multiple(self, words):
        for word in words:
            self.insert(word)

class Node:

    def __init__(self):
        self.children = {}
        self.endOfWord = False
    """Formats all nodes as a dict and is printed as a json."""
    def printNodes(self):
        printVal = {}
        for child in self.children:
            if self.endOfWord == False:
                printVal[child] = self.children[child].printNodes()
            else:
                return {}
        print(json.dumps(printVal))

"""Reads all lines from the given file name."""
def readTheFile(fileName) -> list[str]:
    with open(fileName, "r") as file:
        lines = file.readlines();
    return lines


"""Removes all \n characters from list of words read in by readTheFile()"""
def removeSlashN(word) -> str:
    return word.replace("\n","")

#read in words
result = list(map(removeSlashN, readTheFile("words.txt")))

#Create trie and insert all words
trie = Trie()
trie.insert_multiple(result)
print("done")

#Time searching for last word in words.txt for trie find() and list search

start = time.time()
trie.find("zzzs")
end = time.time()

print(end - start)

start = time.time()
result.index("zzzs")
end = time.time()

print(end - start)
