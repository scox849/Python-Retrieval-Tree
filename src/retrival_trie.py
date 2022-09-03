from typing import List
import json
import time
import pytest
import sys

class Trie:
    """Implementation of a retriveal tree."""

    def __init__(self):
        self.root = Node()

    def __str__(self):
        return json.dumps(self.root.format_nodes_for_print(), indent=2)

    def insert(self, word):
        """Inserts a single word into the tree. If the word already exists it will not be
           inserted more than once."""

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

    def find(self, word):
        """Finds the given word in the trie. Only searches for whole words. Return true of false based on existance."""

        currentNodeChildren = self.root.children
        word_idx = 0
        word_length = len(word)

        for letter in word:
            if currentNodeChildren.get(letter) is not None:
                if currentNodeChildren.get(letter).endOfWord == True and word_length == (word_idx + 1):
                    return True
                else:
                    currentNodeChildren = currentNodeChildren.get(letter).children
                    word_idx += 1
            else:
                return False

    def insert_multiple(self, words):
        """Inserts multiple words into trie."""

        return list(map(self.insert, words))

class Node:

    def __init__(self):
        self.children = {}
        self.endOfWord = False


    def format_nodes_for_print(self):
        """Formats all nodes as a dict and is printed as a json."""

        printVal = {}
        for child in self.children:
            if self.endOfWord == False:
                printVal[child] = self.children[child].format_nodes_for_print()
            else:
                return {}
        return printVal


def readTheFile(fileName) -> list[str]:
    """Reads all lines from the given file name."""

    with open(fileName, "r") as file:
        lines = file.readlines();
    return lines


def removeSlashN(word) -> str:

    """Removes all \n characters from list of words read in by readTheFile()"""
    return word.replace("\n","")


def test_all():
    """Test by inserting all words into trie and then searching and finding each word inserted."""

    trie = Trie()
    result = list(map(removeSlashN, readTheFile("words.txt")))
    trie.insert_multiple(result)
    all_found = []
    for word in result:
        found = trie.find(word)
        all_found.append(found)
    assert all(all_found) == True



def main(args: List[str]):
    """Inserts words into trie base on file name provided, then
       searches for words input by the user."""

    if len(args) < 2:
        print("Please provide a file path to words file.")
        return
    if len(args) > 2:
        print("Too many arguments. Please provide file path only.")
        return

    trie = Trie()
    result = list(map(removeSlashN, readTheFile(args[1])))
    trie.insert_multiple(result)

    print("Type '--exit' to exit.")
    user_input = input("Enter a word to find: ")

    while user_input != '--exit':

        start = time.time()
        found = trie.find(user_input.lower())
        end = time.time()
        total_time = end - start

        if found:
            print("Found", user_input, "in:", total_time, "seconds.")
        else:
            print(user_input, "not in trie.")

        user_input = input("Enter a word to find: ")

if __name__ == "__main__":

    main(sys.argv)
