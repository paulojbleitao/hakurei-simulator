from collections import defaultdict, Counter
import random
import pickle

END = 0

class Markov:
    def __init__(self):
        self.word_dict = self.load_data()

    def make_pairs(self, message):
        words = message.split()
        words = list(filter(lambda word: not self.is_mention(word), words))
        for i in range(len(words)):
            if i == len(words) - 1:
                yield (words[i], END)
            else:
                yield (words[i], words[i + 1])

    def is_mention(self, word):
        return word.startswith('<@') and word.endswith('>')

    def add_message(self, message):
        pairs = self.make_pairs(message)
        for word1, word2 in pairs:
            self.word_dict[word1][word2] += 1
        self.save_data()

    def generate_message(self):
        first_word = random.choice(list(self.word_dict))
        chain = [first_word]

        while chain[-1] != END and len(chain) < 30:
            current_word = self.word_dict[chain[-1]]
            next = list(current_word)
            weights = list(current_word.values())
            chain.append(random.choices(next, weights)[0])
        
        if chain[-1] == END: chain.pop()
        return ' '.join(chain)

    def save_data(self):
        with open('data.pickle', 'wb') as f:
            pickle.dump(self.word_dict, f, pickle.HIGHEST_PROTOCOL)

    def load_data(self):
        try:
            with open('data.pickle', 'rb') as f:
                return pickle.load(f)
        except:
            return defaultdict(Counter)
