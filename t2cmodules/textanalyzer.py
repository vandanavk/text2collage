import re
import string
from time import time
import os
import nltk
import inflect
from rake_nltk import Rake
import codecs


class TextAnalyzer:
    def tokenize(self, text):
        """

        :param t: Input text
        Save input text and tokenize into sentences.
        """
        self.text = text
        self.sentences = nltk.sent_tokenize(self.text)
        self.phraseScore = []

    def main(self, text):
        self.inflectengine = inflect.engine()
        self.tokenize(text)

        f = codecs.open('stopwords.txt', encoding='utf-8')
        stopw = f.read()
        stopwords = stopw.split(',')
        self.r = Rake(stopwords)
        self.getPhraseScore()

        return self.getKeywords(), self.phraseScore

    def getKeywords(self):
        """
        Extract keywords using POS tagging
        :return: Query keywords
        """
        nouns = []
        tags = []

        for s in self.sentences:
            s = re.sub('[' + string.punctuation + ']', '', s)
            tokens = nltk.tokenize.word_tokenize(s)
            tagged = nltk.pos_tag(tokens)
            sent_kw = []
            sent_tag = []
            for item, t in tagged:
                if 'NN' in t:
                    if len(item) > 1:
                        if self.inflectengine.singular_noun(item) not in sent_kw and self.inflectengine.plural(item) not in sent_kw:
                            sent_kw.append(item)
                        if self.inflectengine.singular_noun(item) not in sent_tag and self.inflectengine.plural(item) not in sent_tag:
                            sent_tag.append(item)
                if 'JJ' in t:
                    if len(item) > 1:
                        if self.inflectengine.singular_noun(item) not in sent_tag and self.inflectengine.plural(item) not in sent_tag:
                            sent_tag.append(item)

            nouns.append(sent_kw)
            tags.append(sent_tag)
        return (nouns, tags)

    def getPhraseScore(self):
        """
        Extract phrase score from the text using RAKE
        """
        for s in self.sentences:
            s = re.sub('[' + string.punctuation + ']', '', s)
            self.r.extract_keywords_from_text(s)
            self.phraseScore.append(self.r.get_ranked_phrases_with_scores())

