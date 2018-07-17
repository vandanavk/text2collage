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

        return self.getKeywords(), self.getTags(), self.phraseScore

    def getTags(self):
        """
        Extract possible tags from the text using RAKE
        :return: Tag set
        """
        meaningset = []
        if len(self.sentences) == 1:
            s = re.sub('[' + string.punctuation + ']', '', self.sentences[0])
            self.r.extract_keywords_from_text(s)
            rp = self.r.get_ranked_phrases()
            self.phraseScore.append(self.r.get_ranked_phrases_with_scores())
            final_nouns = []
            for n in rp:
                tokens = nltk.tokenize.word_tokenize(n)
                if len(tokens) == 1:
                    item, tag = nltk.pos_tag(tokens)[0]
                    if 'NN' in tag:
                        if len(item) > 1:
                            if self.inflectengine.singular_noun(item) not in final_nouns and self.inflectengine.plural(item) not in final_nouns:
                                final_nouns.append(item)
                else:
                    final_nouns.append(n)
            return final_nouns

        for s in self.sentences:
            s = re.sub('[' + string.punctuation + ']', '', s)
            self.r.extract_keywords_from_text(s)
            rp = self.r.get_ranked_phrases()
            self.phraseScore.append(self.r.get_ranked_phrases_with_scores())
            final_nouns = []
            for n in rp:
                tokens = nltk.tokenize.word_tokenize(n)
                if len(tokens) == 1:
                    item, tag = nltk.pos_tag(tokens)[0]
                    if 'NN' in tag:
                        if len(item) > 1:
                            if self.inflectengine.singular_noun(item) not in final_nouns and self.inflectengine.plural(item) not in final_nouns:
                                final_nouns.append(item)
                else:
                    final_nouns.append(n)
            meaningset.append(final_nouns)
        return meaningset

    def getKeywords(self):
        """
        Extract keywords using POS tagging
        :return: Query keywords
        """
        nouns = []
        if len(self.sentences) == 1:
            s = re.sub('[' + string.punctuation + ']', '', self.sentences[0])
            self.r.extract_keywords_from_text(s)
            rp = self.r.get_ranked_phrases()
            for n in rp:
                tokens = nltk.tokenize.word_tokenize(n)
                if len(tokens) == 1:
                    item, tag = nltk.pos_tag(tokens)[0]
                    if 'NN' in tag:
                        if len(item) > 1:
                            if self.inflectengine.singular_noun(item) not in nouns and self.inflectengine.plural(item) not in nouns:
                                nouns.append(item)
                else:
                    nouns.append(n)
            return nouns
        for s in self.sentences:
            s = re.sub('[' + string.punctuation + ']', '', s)
            tokens = nltk.tokenize.word_tokenize(s)
            tagged = nltk.pos_tag(tokens)
            final_nouns = []
            for item, t in tagged:
                if 'NN' in t:
                    if len(item) > 1:
                        if self.inflectengine.singular_noun(item) not in final_nouns and self.inflectengine.plural(item) not in final_nouns:
                            final_nouns.append(item)
            nouns.append(final_nouns)
        return nouns

    # def getKeywords(self):
    #     """
    #     Extract keywords using POS tagging
    #     :return: Query keywords
    #     """
    #     nouns = []
    #     tags = []
    #
    #     if len(self.sentences) == 1:
    #         s = re.sub('[' + string.punctuation + ']', '', self.sentences[0])
    #         self.r.extract_keywords_from_text(s)
    #         rp = self.r.get_ranked_phrases()
    #         for n in rp:
    #             tokens = nltk.tokenize.word_tokenize(n)
    #             if len(tokens) == 1:
    #                 item, tag = nltk.pos_tag(tokens)[0]
    #                 if 'NN' in tag:
    #                     if len(item) > 1:
    #                         if self.inflectengine.singular_noun(item) not in nouns and self.inflectengine.plural(item) not in nouns:
    #                             nouns.append(item)
    #             else:
    #                 nouns.append(n)
    #         return nouns
    #     for s in self.sentences:
    #         s = re.sub('[' + string.punctuation + ']', '', s)
    #         tokens = nltk.tokenize.word_tokenize(s)
    #         tagged = nltk.pos_tag(tokens)
    #         sent_kw = []
    #         sent_tag = []
    #         for item, t in tagged:
    #             if 'NN' in t:
    #                 if len(item) > 1:
    #                     if self.inflectengine.singular_noun(item) not in sent_kw and self.inflectengine.plural(item) not in sent_kw:
    #                         sent_kw.append(item)
    #                     if self.inflectengine.singular_noun(item) not in sent_tag and self.inflectengine.plural(item) not in sent_tag:
    #                         sent_tag.append(item)
    #             if 'JJ' in t:
    #                 if len(item) > 1:
    #                     if self.inflectengine.singular_noun(item) not in sent_tag and self.inflectengine.plural(item) not in sent_tag:
    #                         sent_tag.append(item)
    #
    #         nouns.append(sent_kw)
    #         tags.append(sent_tag)
    #     return (nouns, tags)

    def getPhraseScore(self):
        """
        Extract phrase score from the text using RAKE
        """
        for s in self.sentences:
            s = re.sub('[' + string.punctuation + ']', '', s)
            self.r.extract_keywords_from_text(s)
            self.phraseScore.append(self.r.get_ranked_phrases_with_scores())

