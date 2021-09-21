from collections import Counter
from nltk.corpus import wordnet as wn


class TextMethods:
    def __init__(self, text: str):
        self.text = text
        self.freq = None
        self.nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
        self.verbs = {x.name().split('.', 1)[0] for x in wn.all_synsets('v')}

    def frequency(self):
        self.freq = Counter(self.text
                            .replace('.', ' ')
                            .replace(',', ' ')
                            .replace('!', ' ')
                            .replace('?', ' ')
                            .replace('\n', ' ')
                            .split(' '))

    @staticmethod
    def cut_the_word(text: str, word: str):
        return text \
            .replace(' ' + word + ' ', ' ') \
            .replace(' ' + word + '.', ' .') \
            .replace(' ' + word + ',', ' ,') \
            .replace(' ' + word + '!', ' !') \
            .replace(' ' + word + '?', ' ?') \
            .replace('.' + word + ' ', '. ') \
            .replace(',' + word + ' ', ', ') \
            .replace('!' + word + ' ', '! ') \
            .replace('?' + word + ' ', '? ')

    def update_text_delete_words(self):
        self.text = TextMethods.cut_the_word(self.text, 'any')
        self.text = TextMethods.cut_the_word(self.text, 'a')
        self.text = TextMethods.cut_the_word(self.text, 'the')

    def update_text_delete_punctuations(self):
        self.text = self.text.replace('.', '') \
            .replace(',', '') \
            .replace('!', '') \
            .replace('?', '') \
            .replace('\n', '')

    @staticmethod
    def prepare_phrase(phrase: str):
        return phrase.replace('.', ' ') \
            .replace(',', ' ') \
            .replace('!', ' ') \
            .replace('?', ' ') \
            .replace('\n', ' ') \
            .split()

    def count_matches(self, phrase: str):
        hash_dict = {word: hash(word) for word in self.freq}
        list_of_words_from_text = TextMethods.prepare_phrase(self.text)
        while list_of_words_from_text.__contains__(' '):
            list_of_words_from_text.remove(' ')
        list_of_words_from_phrase = TextMethods.prepare_phrase(phrase)
        while list_of_words_from_phrase.__contains__(' '):
            list_of_words_from_phrase.remove(' ')

        for word in list_of_words_from_phrase:
            if word not in hash_dict:
                return 0
        count = 0
        text_len = len(list_of_words_from_text)
        pattern_len = len(list_of_words_from_phrase)
        for i in range(text_len - pattern_len):
            for j in range(pattern_len):
                if hash_dict[list_of_words_from_text[i + j]] == hash_dict[list_of_words_from_phrase[j]]:
                    if j == pattern_len - 1:
                        count += 1
                else:
                    break
        return count

    def find_some_phrase_with_noun(self):
        list_of_words_from_text = TextMethods.prepare_phrase(self.text)
        phrases = []
        for i in range(len(list_of_words_from_text) - 1):
            if list_of_words_from_text[i] in self.verbs and list_of_words_from_text[i + 1] in self.nouns:
                phrases.append(list_of_words_from_text[i] + " " + list_of_words_from_text[i + 1])
        return phrases