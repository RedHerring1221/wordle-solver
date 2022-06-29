import json


class Node:
    def __init__(self):
        self.children = {}
        self.word = ""

    def dfs(self, level):
        # if we have reached a full 5 letter word, and there are no needed letters left to add, add this is a valid word
        if level == 5:
            if not needed_letters:
                words.append(self.word)
            return
        # get valid letters that could be the next letter in word
        letters_to_search = []
        if correct_letters[level]:
            letters_to_search.append(correct_letters[level])
        else:
            for letter in self.children.keys():
                if letter not in incorrect_letters[level]:
                    letters_to_search.append(letter)
        # search for all possible words using the valid letters, removing a needed letter if used
        for letter in letters_to_search:
            if letter in self.children:
                flag = False
                if letter in needed_letters:
                    flag = True
                    if needed_letters[letter] == 1:
                        del needed_letters[letter]
                    else:
                        needed_letters[letter] -= 1

                self.children[letter].dfs(level + 1)

                # add needed letter back if it was used to backtrack
                if flag:
                    needed_letters[letter] = 1 if letter not in needed_letters else needed_letters[letter] + 1


class Trie:
    def __init__(self):
        self.root = Node()

    # add a word to the Trie
    def add(self, word):
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = Node()
            curr = curr.children[ch]
        curr.word = word

    # search through the trie and add all possible words to the words list
    def search(self):
        self.root.dfs(0)


# validate that the inputted word is 5 letters longs and only contains lowercase letters
def check_word(word):
    return len(word) == 5 and word.islower() and word.isalpha()


# check the colors inputted is 5 characters long and only contains g y and b
def check_colors(colors):
    if len(colors) != 5:
        return False
    for c in colors:
        if c not in ['g', 'y', 'b']:
            return False
    return True


# based on the guessed word and colors returned, update the correct_letters, incorrect_letters and needed_letters
# variables accordingly. temp is a temporary dictionary to compare against needed_letters. For each guess we keep the
# maximum number of instances of a needed letter
def update(word, colors):
    temp = {}
    for i, color in enumerate(colors):
        if color == 'g':
            temp[word[i]] = 1 if word[i] not in temp else temp[word[i]] + 1
            correct_letters[i] = word[i]
        elif color == 'y':
            temp[word[i]] = 1 if word[i] not in temp else temp[word[i]] + 1
            incorrect_letters[i].append(word[i])
        else:
            if word[i] in temp:
                incorrect_letters[i].append(word[i])
            else:
                for j in range(5):
                    incorrect_letters[j].append(word[i])
    for letter in temp:
        needed_letters[letter] = temp[letter] if letter not in needed_letters else max(temp[letter], needed_letters[letter])


# output the top 100 words in rows of 20
def output(words):
    print()
    i = 0
    while i < len(words) and i < 100:
        line = ""
        j = i
        while j < i + 20 and j < len(words):
            line += words[j] + ", "
            j += 1
        print(line)
        i += 20


if __name__ == "__main__":
    trie = Trie()
    correct_letters = [None, None, None, None, None]
    needed_letters = {}
    incorrect_letters = [[], [], [], [], []]
    words = []
    frequencies = {}
    turn = 1

    # add words to the trie and frequencies to the freq dictionary
    with open("word_frequencies.json", 'r') as read_file:
        data = json.load(read_file)
    for word in data.keys():
        freq = data[word]
        trie.add(word)
        frequencies[word] = int(freq)

    # simulate the turns the player takes in wordle.
    while turn <= 7:
        if turn == 7:
            if len(words) == 1:
                print("Sorry! Took to many turns. The wordle of the day is", words[0])
            else:
                print("Sorry, could not find the wordle of the day.")
            break
        words.clear()

        # get user input
        print("Guess", turn)
        word = ""
        while not check_word(word):
            word = input("Enter guessed word: ")
            if not check_word(word):
                print("Please input a 5 letter word using only lowercase letters")
        colors = ""
        while not check_colors(colors):
            colors = input("Please enter the color of the tiles. (Ex gybby): ")
            if not check_colors(colors):
                print("Please enter 5 letters representing the colors. green = g, yellow = y, black = b")

        # update possible letters and search for possible words, then sort based on word frequency
        update(word, colors)
        trie.search()
        words = sorted(words, key=lambda word: frequencies[word], reverse=True)

        if len(words) == 1:
            print("Congratulations! The wordle of the day is", words[0])
            break
        if len(words) == 0:
            print("An error has occurred, check your inputs for mistakes, otherwise the word is not in our dictionary")
            break

        output(words)
        print(len(words), "possible words\n")
        turn += 1
