import datetime
from collections import Counter

from django.db import models
from django.utils import timezone
from random import *
import spacy


class Thesis:
    def __init__(self, ideas):
        self.ideas = ideas

    def __str__(self):
        return self.build()

    def prepare(self):

        # build evidences

        fact = self.ideas.get("fact", "")

        definition = self.ideas.get("definition", "")

        quality = self.ideas.get("quality", "")

        counterpoint = self.ideas.get("counterpoint", "")

        evidences = [fact, definition, counterpoint]

        policy = self.ideas.get("policy", "")

        if quality and policy:
            argument = policy + " " + quality
        else:
            argument = policy + quality

        return {'argument': argument, 'evidences': evidences}


class Draft:
    def __init__(self, elements):
        self.type = ""
        self.structure = ""
        self.elements = elements
        self.argument = elements['argument']
        self.entities = elements['entities']
        self.claims = elements['claims']
        self.evidences = elements['evidences']

    def introduction(self):
        pass

    def generate(self):
        introduction = self.argument
        for c in self.claims:
            introduction += " " + c

        paragraphs = []

        paragraph_what = self.claims[0] + " " + self.evidences[0]
        paragraphs.append(paragraph_what)

        paragraph_nature = self.claims[1] + " " + self.evidences[1]
        paragraphs.append(paragraph_nature)

        if randrange(10) > 5:
            prefix_e = "One might object here that"
            prefix_c = "Nevertheless,"
        else:
            prefix_e = "On the one hand, I agree with some proponents that"
            prefix_c = "But on the other hand, I still insist that"
        counter_evidence = self.pack(prefix_e, self.evidences[2])
        counter_claim = self.pack(prefix_c, self.claims[2])

        paragraph_counter = counter_evidence + " " + counter_claim
        paragraphs.append(paragraph_counter)

        conclusion = introduction
        return {'introduction': introduction, 'paragraphs': paragraphs, 'conclusion': conclusion}

    def pack(self, prefix, sentence):
        packed = sentence
        first_word = packed.split(' ', 1)[0]
        if first_word not in self.entities:
            packed = packed[0].lower() + packed[1:]
        return prefix + " " + packed


# model for transition
class Transition:
    def __init__(self, category):
        self.category = category  # e.g., contrast

    def get_category(self):
        return self.category

    def get_phrases(self):
        """
        :param category: string
        :return (list): list of words in the given category
        """
        phrases = []

        cause_effect = ["Consequently", "Therefore", "Accordingly", "As a result",
                        "Hence", "Thus", "For this reason", "Due"]
        sequence = ["Furthermore", "In addition", "Moreover", "Finally",
                    "Again", "Until then", "In light of", "Again"]
        compare_contrast = ["similarly", "Likewise", "In the same fashion", "In the same way",
                            "In like manner", "Correspondingly", "Equally important", "Conversely", "In contrast",
                            "however", "On the contrary", "yet", "whereas"]
        example = ["For instance", "For example", "In fact", "Indeed", "of course",
                   "Equally important", "Specifically", "In other words"]
        purpose = ["Ultimately", "Evidently", "Without doubt", "Invariably", "To this end"]
        multiple = ["Couples with", "Together with", "vast array", "tapestry", "plethora"]

        if self.category == "cause_effect":
            phrases = cause_effect

        if self.category == "sequence":
            phrases = sequence

        return phrases

    def get_phrase(self):
        phrases = self.get_phrases()
        i = randrange(len(phrases))
        return phrases[i]


# model for active verbs
class Verb:
    def __init__(self, category):
        self.category = category

    def get_category(self):
        return self.category

    def get_verbs(self):
        """
        :param category: string
        :return (list): list of words in the given category
        """
        verbs = []

        literary = ["Consequently", "Therefore", "Accordingly", "As a result",
                    "Hence", "Thus", "For this reason", "Due"]
        research = ["Furthermore", "In addition", "Moreover", "Finally",
                    "Again", "Until then", "In light of", "Again"]
        beginnings = ["similarly", "Likewise", "In the same fashion", "In the same way",
                      "In like manner", "Correspondingly", "Equally important", "Conversely", "In contrast",
                      "however", "On the contrary", "yet", "whereas"]
        ideas = ["For instance", "For example", "In fact", "Indeed", "of course",
                 "Equally important", "Specifically", "In other words"]
        legal = ["Ultimately", "Evidently", "Without doubt", "Invariably", "To this end"]

        if self.category == "literary":
            verbs = literary

        if self.category == "beginnings":
            verbs = beginnings

        return verbs

    def get_verb(self):
        verbs = self.get_verbs()
        i = randrange(len(verbs))
        return verbs[i]


class Assignment:
    informative = ['inform', 'describe', 'define', 'review', 'notify', 'instruct', 'advise', 'announce', 'explain',
                   'demonstrate', 'illustrate', 'discuss', 'analyse', 'analyze']
    persuasive = ['persuade', 'convince', 'influence', 'argue', 'recommend', 'change', 'advocate', 'urge', 'defend',
                  'justify', 'support', 'to what extent', 'assess', 'evaluate', 'affect']

    subjects = ['Hitler', 'Mao', 'economic', 'finance']

    def __init__(self, assignment):
        self.purpose = "persuasive"
        self.topic = ""
        self.assignment = assignment

    def process(self):
        info = 0
        pers = 0
        for word in self.assignment.split():
            if word in self.informative:
                info += 1
            if word in self.persuasive:
                pers += 1
            if word in self.subjects:
                self.topic += word + " "
        if info > pers:
            self.purpose = "informative"

        return self

    def get_purpose(self):
        return self.purpose

    def get_topic(self):
        return self.topic


class Idea:
    questions = [
        # Facts
        "{F}How did it begin and what are the causes?",
        "{F}What happened to {ENTS}?",
        "{F}What is the story behind {ENTS}?",
        "{F}What do we know about \"{SUBJ}\"?",
        "{F}What happened to \"{SUBJ}\"?",
        "{F}What do we know about {SUBJ} and {OBJ}?",
        "{F}Any knowledge about \"{SUBJ}\" and \"{OBJ}\"?",

        # Definition
        "{D}What are its parts, and how are they related?",
        "{D}What is the nature of \"{SUBJ}\"?",
        "{D}What are the components of \"{SUBJ}?\"",
        "{D}What are the attributes of \"{OBJ}\"?",
        "{D}What are similar concepts to \"{OBJ}\"?",
        "{D}How are \"{SUBJ}\" and \"{OBJ}\" related?",
        "{D}What are similar concepts to \"{SUBJ}\" and \"{OBJ}\"?",

        # Quality
        "{Q1}Is it good or bad?",
        "{Q2}What would be a different evaluation on \"{SUBJ}\"?",
        "{Q1}Is \"{SUBJ}\" positive or negative?",
        "{Q2}What if we measure \"{SUBJ}\" differently?",
        "{Q1}What role does \"{OBJ}\" serve?",
        "{Q1}Opinion about \"{OBJ}\" in the topic?",
        "{Q2}Any different measurement about \"{OBJ}\"?",

        # Policy
        "{P}With previous ideas, what do you want to advocate?",
        "{P}Suggestion about \"{SUBJ}\" and \"{OBJ}\"?",
        "{P}What do you want to advocate about the \"{SUBJ}\"?",
    ]

    def __init__(self, topic):
        self.topic = topic
        self.subject = ""
        self.verb = ""
        self.object = ""
        self.entities = []
        self.processed = False

    def blocked(self):
        if '</script>' in self.topic:
            return True

        blacklist = [
            "test",
            "thisisatest",
            "whatsup",
        ]
        topic = ''.join(e for e in self.topic if e.isalnum()).lower()
        if topic.isdigit() or topic in blacklist or len(topic) < 2:
            return True

        if not self.processed:
            self.process()
        if not self.subject and not self.object and not len(self.entities):
            return True
        return False

    def process(self):
        if self.processed:
            return self

        nlp = spacy.load('en_core_web_sm')
        doc = nlp(self.topic)
        sentence = next(doc.sents)  # last sentence in prompt

        for word in sentence:
            if word.dep_ == 'nsubj':
                self.subject = word.text
            if word.dep_ in ['dobj', 'obj']:
                self.object = word.text
            if word.dep_ == 'ROOT':
                if word.pos_ == 'VERB':
                    self.verb = word.text.lower()
                if word.pos_ == 'NOUN' and not self.subject:
                    self.subject = word.text.lower()

        if self.subject:
            for chunk in doc.noun_chunks:
                if self.subject in chunk.text:
                    self.subject = chunk.text
                    break

        if self.object:
            for chunk in doc.noun_chunks:
                if self.object in chunk.text:
                    if 'What' not in chunk.text and 'Which' not in chunk.text:
                        self.object = chunk.text
                    break

        entities = []
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'ORG', 'EVENT', 'GPE', 'NORP']:
                entities.append(ent.text)

        ents = ""
        num_ents = len(entities)
        if num_ents:
            ents = entities[0]
            if num_ents == 2:
                ents += " and " + entities[1]
            elif num_ents > 2:  # 3 and more
                for i in range(1, num_ents - 1):
                    ents += ", " + entities[i]
                ents += ", and " + entities[num_ents - 1]

        self.entities = ents

        self.processed = True
        return self

    def generate_questions(self):

        qs = []

        # replaced with subj, obj, and entities
        for q in self.questions:
            qs.append(q.replace('{SUBJ}', '--' + self.subject + '--').
                      replace('{OBJ}', '--' + self.object + '--').
                      replace('{ENTS}', '--' + self.entities + '--'))

        # filter
        shuffle(qs)
        q_fact = ['']
        q_definition = ['']
        q_quality = [''] * 2
        q_policy = ['']
        for q in qs:
            if '----' not in q:
                if '{F}' in q and not q_fact[0]:
                    q_fact[0] = q.replace('{F}', '').replace('--', '')
                if '{D}' in q and not q_definition[0]:
                    q_definition[0] = q.replace('{D}', '').replace('--', '')
                if '{Q1}' in q and not q_quality[0]:
                    q_quality[0] = q.replace('{Q1}', '').replace('--', '')
                if '{Q2}' in q and not q_quality[1]:
                    q_quality[1] = q.replace('{Q2}', '').replace('--', '')
                if '{P}' in q and not q_policy[0]:
                    q_policy[0] = q.replace('{P}', '').replace('--', '')

        questions = q_fact + q_definition + q_quality  # + q_policy

        return questions

    def build_questions(self):
        return {'questions': self.generate_questions()}


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

    def common_words(self, n=5):
        doc = self.nlp(self.content.replace('<br>', ' '))
        # remove stopwords and punctuations
        words = [token.text for token in doc if token.is_stop != True and token.is_punct != True]
        word_freq = Counter(words)
        common_words = word_freq.most_common(n)
        return common_words
