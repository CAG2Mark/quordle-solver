from collections import defaultdict

words = [x.strip() for x in open("words").readlines()]
possible = [x.strip() for x in open("possible_words").readlines()]

class Game:
    def __init__(self, word):
        self.word = word

    def guess_word(self, guess):
        d = defaultdict(lambda: 0)
        ret = list("00000")

        for ch in self.word:
            d[ch] += 1

        for i, ch in enumerate(self.word):
            if guess[i] == self.word[i]:
                ret[i] = "2"
                d[ch] -= 1

        for i, ch in enumerate(guess):
            if ret[i] == "2": continue

            if d[ch] != 0:
                ret[i] = "1"
                d[ch] -= 1
            else:
                ret[i] = "0"

        return ''.join(ret)
