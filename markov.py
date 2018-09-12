from collections import defaultdict, Counter
import random
import pickle

START = 1
END = 0

class Markov:
    def __init__(self):
        self.word_dict = self.load_word_data()
        self.users_dict = self.load_users_data()

    def make_pairs(self, message):
        words = message.split()
        words = list(filter(lambda word: self.is_valid(word), words))
        start_index = -1 if len(words) > 0 else 0
        for i in range(start_index, len(words)):
            if i == -1:
                yield (START, words[i + 1])
            elif i == len(words) - 1:
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

    def add_words(self, message):
        pairs = self.make_pairs(message)
        for word1, word2 in pairs:
            self.word_dict[word1][word2] += 1
        
    def add_user_stats(self, message, author):
        words = message.split()
        for word in words:
            self.users_dict[word][author] += 1

    def add_message(self, message, author):
        self.add_words(message)
        self.add_user_stats(message, author)
        self.save_data()

    def generate_message(self):
        first_word = START
        chain = [first_word]

        while chain[-1] != END:
            current_word = self.word_dict[chain[-1]]
            next = list(current_word)
            weights = list(current_word.values())
            chain.append(random.choices(next, weights)[0])
        
        chain = chain[1:-1]
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

    def count_occurrences(self, word):
        total = 0
        for w in self.word_dict:
            if word in self.word_dict[w]:
                total += self.word_dict[w][word]
    
        return total

    def person_who_used_most(self, word):
        result = ''
        if len(self.users_dict[word]) > 0:
            person, x = self.users_dict[word].most_common(1)[0]
            result = f'The person who used it the most is {person} ({x} times)!'
        else:
            result = "I don't remember seeing anyone use that word..."

        return result

    def word_statistics(self, word):
        n = self.count_occurrences(word)
        person = self.person_who_used_most(word)
        stats = (
            f'The word `{word}` has been used {n} times!\n'
            f'{person}'
        )
        return stats

    def save_data(self):
        with open('data.pickle', 'wb') as f:
            pickle.dump(self.word_dict, f, pickle.HIGHEST_PROTOCOL)

        with open('users_data.pickle', 'wb') as f2:
            pickle.dump(self.users_dict, f2, pickle.HIGHEST_PROTOCOL)

    def load(self, file):
        try:
            with open(f'{file}.pickle', 'rb') as f:
                return pickle.load(f)
        except:
            return defaultdict(Counter)

    def load_word_data(self):
        return self.load('data')

    def load_users_data(self):
        return self.load('users_data')
