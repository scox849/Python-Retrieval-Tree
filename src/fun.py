from typing import Dict, Optional, Union, List
from os import path
import json
import time


class Trie:
    """Implementation of a retriveal tree."""

    def __init__(self):
        self.root = Node()

    def insert(self, word : str ) -> None:
        """Inserts a single word into the tree. If the word already exists it will not be
        inserted more than once.
        """

        if word == "":
            return

        childs : Dict = self.root.children
        lastNode : Optional[Node]
        letter : str
        for letter in word:

            if letter in childs:
                newNode = childs[letter]
            else:
                newNode = Node()
                childs[letter] = newNode
            childs = newNode.children
            lastNode = newNode

        lastNode.endOfWord = True

    def find(self, word) -> bool:
        """Finds the given word in the trie. Only searches for whole words. Return true of false based on existance."""
        currentNodeChildren : Dict[str, Node] = self.root.children
        l : Node
        for letter in word:
            l = currentNodeChildren.get( letter )
            if l is not None and l.endOfWord == True:
                return True
            elif l is None or l.children is None :
                return False
            else :
                currentNodeChildren = l.children

    """Inserts multiple words into trie."""
    def insert_multiple(self, words) -> None:

        return next(
            (
                result
                for result in (
                    self.insert(word)
                    for word in words
                )
                if result is not None
            ),
            None
        )

class Node:

    def __init__(self):
        self.children : Dict[str,Node] = {}
        self.endOfWord : bool = False

    def serialize(self) -> Union[str,Dict] :
        """Formats all nodes as a dict and is printed as a json."""

        printVal : Dict = {}
        for child in self.children:
            if self.endOfWord == False:
                printVal[child] = self.children[child].serialize()
            else:
                return {}

        return printVal

    def __str__(self) -> str :

        return json.dumps( self.serialize(), indent = 2 )



"""Reads all lines from the given file name."""
def readTheFile(fileName):
    with open( path.join( path.dirname( __file__ ), fileName ), "r") as file:
        return file.readlines()


"""Removes all \n characters from list of words read in by readTheFile()"""
def removeSlashN(word):
    return word.replace("\n","")

def _main() :
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

    print( trie.root )


def main( args : List[str] ) :
    """Pass in a list of arguements, the first of which is the item to be searched
    for.
    """

    findable = args[0]
    searchable = args[1:]

    t = Trie()

    # Timed insertion
    start = time.time()
    t.insert_multiple( searchable )
    end = time.time()

    f_start = time.time()
    was_found = t.find( findable )
    f_end = time.time()

    # Serialize results 
    results : Dict = {
        "insert_time_start" : start,
        "insert_time_end" : end,
        "insert_time_duration" : end - start,
        "found" : {
            "find" : findable,
            "find_start_time" : f_start,
            "find_end_time" : f_end,
            "find_time_duration" : f_end - f_start,
            "was_found" : was_found
        }
    }
    print(json.dumps( results, indent = 2 ))


if __name__ == "__main__" :

    from sys import argv
    main(argv[1:])
