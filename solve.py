from collections import defaultdict
import numpy as np

guess_table = None
class Solver:

    def __init__(self, N):
        self.N = N
        self.first = True

        global guess_table

        if not guess_table:
            guess_table = {}
            # Load the guess lookup table
            with open("guess_table") as f:                
                answers = []
                first = True
                for l in f:
                    l = l.strip()
                    l = l.split(",")
                    first_entry = l[0]
                    contents = l[1:]
                    if first:
                        for answer in contents: guess_table[answer] = {}
                        answers = contents
                        first = False
                        continue
                    
                    for i, result in enumerate(contents):
                        guess_table[answers[i]][first_entry] = result
                    
        with open("words") as word_f:
            self.words_all = np.array([x.strip() for x in word_f.readlines()])
        with open("possible_words") as possible_f:
            words_possible = np.array([x.strip() for x in possible_f.readlines()])
        
        # don't use np array as could be jagged
        self.words_possible = [np.array(words_possible) for _ in range(N)]
        self.solved = [False]*N

    def filter_word(self, guess_word, responses):
        self.first = False
        # 0 = wrong
        # 1 = correct, wrong pos
        # 2 = correct

        for i in range(self.N):
            possible_list = self.words_possible[i]
            response = responses[i]

            chars = defaultdict(lambda: 0)
            for j, ch in enumerate(guess_word): 
                if response[j] > 0: chars[ch] += 1
            
            bool_arr = np.array(
                [self.is_word_ok(word, guess_word, response, chars) for word in possible_list]
                )
            if len(bool_arr) == 0: continue

            self.words_possible[i] = possible_list[bool_arr]
         
    @staticmethod
    def is_word_ok(word, guess_word, response, chars):
        for i, r in enumerate(response):
            ch = guess_word[i]
            if r == 1 and word[i] == ch: return False
            if r == 2 and word[i] != ch: return False
        for i, r in enumerate(response):
            ch = guess_word[i]
            if (r == 0) and (ch in word) and (chars[ch] == 0): return False

        for char, cnt in chars.items():    
            if word.count(char) < cnt: return False
            # print(f"{word} passed step 4")
        # print("true!")
        return True

    @staticmethod
    def compute_guess_quality(word, possible_words):
        probs = np.zeros(243)
        for possible in possible_words:
            res = int(guess_table[possible][word], 3)
            probs[res] += 1
        
        probs /= probs.sum()
        probs = probs[probs != 0]
        # Calculate information
        information = -np.log2(probs)
        # Calculate expected information
        expected_info = np.sum(probs * information)
        return expected_info

    def get_best_guess_quality(self):
        guess = self.get_best_guess()
        info = sum([self.compute_guess_quality(guess, l) for l in self.words_possible])
        return guess, info

    def get_best_guess(self):
        if self.first:
            return "crane"
        # Check if any are solved.
        solved = -1
        for i in range(self.N):
            if len(self.words_possible[i]) == 1:
                solved = i
                break
        if solved != -1:
            word = self.words_possible[i][0]
            del self.words_possible[i]
            self.N -= 1
            return word

        max_info = 0
        best = ""
        for w in self.words_all:
            total_info = 0
            for l in self.words_possible:
                total_info += self.compute_guess_quality(w, l)
            if total_info > max_info: 
                max_info = total_info
                best = w
        return best