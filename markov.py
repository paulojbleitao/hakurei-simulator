from collections import defaultdict, Counter
import random
import pickle

END = 0

class Markov:
    def __init__(self):
        self.word_dict = self.load_data()

    def make_pairs(self, message):
        words = message.split()
        words = list(filter(lambda word: self.is_valid(word), words))
        for i in range(len(words)):
            if i == len(words) - 1:
                yield (words[i], END)
            else:
                yield (words[i], words[i + 1])

    def is_mention(self, word):
        return word.startswith('<@') and word.endswith('>')

    def is_command(self, word):
        return word == 'h!' or word.startswith('!') or word.startswith('.')

    def is_link(self, word):
        return word.startswith('http://') or word.startswith('https://')

    def is_valid(self, word):
        return not (self.is_mention(word)
                    or self.is_command(word)
                    or self.is_link(word))

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

    def word_with_most_links(self):
        top_word = random.choice(list(self.word_dict))
        for word in self.word_dict:
            if len(self.word_dict[word]) > len(self.word_dict[top_word]):
                top_word = word
        return top_word

    def statistics(self):
        n_words = len(list(self.word_dict))
        most_links = self.word_with_most_links()
        stats = (
            f'Right now I know {n_words} unique words!\n'
            f'The word that leads to the most different words is `{most_links}`'
            f' ({len(self.word_dict[most_links])} words)!'
        )
        return stats

    def save_data(self):
        with open('data.pickle', 'wb') as f:
            pickle.dump(self.word_dict, f, pickle.HIGHEST_PROTOCOL)

    def load_data(self):
        try:
            with open('data.pickle', 'rb') as f:
                return pickle.load(f)
        except:
            return defaultdict(Counter)
