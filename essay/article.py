import datetime
from collections import Counter

from django.db import models
from django.utils import timezone
import random
import spacy


class Article:
    def __init__(self, content):
        self.content = content.replace('. <br>', '.<br>').replace('&nbsp;', ' ')
        self.nlp = spacy.load('en_core_web_sm')
        self.simplified = ''
        self.keywords = []

    def process(self):
        self.keywords = self.common_words()

    def parse(self):
        paragraphs = self.content.split('<br>')

        simplified = ""
        for p in paragraphs:
            doc = self.nlp(p.replace("&nbsp;", " "))
            # only keep first and last sentences
            sentences = list(doc.sents)
            n = len(sentences)
            if 0 < n <= 4:
                kept = False
                for w in self.keywords:
                    if w[0].lower() in str(sentences[0]).strip().lower():
                        kept = True
                if kept:
                    simplified += str(sentences[0])
            elif n > 4:
                simplified += " " + str(sentences[0])
                kept = False
                for w in self.keywords:
                    if w[0].lower() in str(sentences[n - 1]).strip().lower():
                        kept = True
                if kept:
                    simplified += str(sentences[n - 1])
            simplified += "\n"
        self.simplified = simplified
        return simplified

    def words(self):
        wc = []
        doc = self.nlp(self.content.replace('<br>', ' '))

        words = [token.text for token in doc]
        wc.append(len(words))
        doc = self.nlp(self.simplified)

        words = [token.text for token in doc]
        wc.append(len(words))
        return wc

    def common_words(self, n=10):
        doc = self.nlp(self.content.replace('<br>', ' '))
        # remove stopwords and punctuations
        words = [token.text.lower() for token in doc if token.is_ascii and not token.is_stop and not token.is_punct and
                 not token.text.isdigit() and len(token.text.strip())]
        word_freq = Counter(words)
        common_words = word_freq.most_common(n)
        return common_words
