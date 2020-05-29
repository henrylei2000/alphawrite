import datetime

from django.db import models
from django.utils import timezone
from random import *
import spacy


class Thesis:
    def __init__(self, ideas):
        self.ideas = ideas

    def __str__(self):
        return self.build()

    def build(self):

        # build evidences
        evidences = []
        fact1 = self.ideas.get("fact1", "")
        fact2 = self.ideas.get("fact2", "")
        e = ""
        if fact1 and fact2:
            e = "Because %s, %s" % (fact2, fact1)
        elif fact1:
            e = fact1
        elif fact2:
            e = fact2
        evidences += [e]

        definition1 = self.ideas.get("definition1", "")
        definition2 = self.ideas.get("definition2", "")
        e = ""
        if definition1 and definition2:
            e = "On one hand, %s. On the other hand, %s" % (definition2, definition1)
        elif definition1:
            e = definition1
        elif definition2:
            e = definition2
        evidences += [e]

        quality1 = self.ideas.get("quality1", "")
        quality2 = self.ideas.get("quality2", "")
        e = ""
        if quality2:
            e = quality2
        evidences += [e]

        policy1 = self.ideas.get("policy1", "")
        policy2 = self.ideas.get("policy2", "")
        argument = ""
        if policy1 and policy2:
            argument = "Even though %s may disagree, %s" % (policy2, policy1)
        elif policy1:
            argument = policy1

        return {'argument': argument, 'evidences': evidences}


class Outline:
    def __init__(self, thesis):
        self.type = ""
        self.structure = ""
        self.thesis = thesis

    def introduction(self):
        pass


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
        "{F1}What is the problem?",
        "{F2}How did it begin and what are the causes?",
        "{F1}What happened to {ENTS}?",
        "{F2}What is the story behind {ENTS}?",
        "{F1}What do we know about {SUBJ}.",
        "{F2}Any knowledge about {SUBJ}?",
        "{F1}What do we know about {SUBJ} and {OBJ}.",
        "{F2}Any knowledge about {SUBJ} and \"{OBJ}\"?",

        # Definition
        "{D1}To what larger class of things does it belong?",
        "{D2}What are its parts, and how are they related?",
        "{D1}What is the nature of {SUBJ}?",
        "{D2}What are the components of {SUBJ}?",
        "{D1}What are the attributes of \"{OBJ}\"?",
        "{D2}What are similar concepts to {OBJ}?",
        "{D1}How are {SUBJ} and \"{OBJ}\" related?",
        "{D2}What are similar concepts to {SUBJ} and {OBJ}?",

        # Quality
        "{Q1}Is it right or wrong?",
        "{Q2}What would be a different evaluation?",
        "{Q1}Is {SUBJ} good or bad?",
        "{Q2}What if we measure {SUBJ} differently?",
        "{Q1}What role does \"{OBJ}\" serve?",
        "{Q2}Any different measurement about {OBJ}?",

        # Policy
        "{P1}Opinion about this topic?",
        "{P2}Who disagrees with you?",
        "{P1}Opinion about {SUBJ}?",
        "{P2}Any arguments against your opinion?",
        "{P1}Opinion about \"{OBJ}\" in the topic?",
        "{P2}Any disagreements about \"{OBJ}\"?",
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
        q_fact = [''] * 2
        q_definition = [''] * 2
        q_quality = [''] * 2
        q_policy = [''] * 2
        for q in qs:
            if '----' not in q:
                if '{F1}' in q and not q_fact[0]:
                    q_fact[0] = q.replace('{F1}', '').replace('--', '')
                if '{F2}' in q and not q_fact[1]:
                    q_fact[1] = q.replace('{F2}', '').replace('--', '')
                if '{D1}' in q and not q_definition[0]:
                    q_definition[0] = q.replace('{D1}', '').replace('--', '')
                if '{D2}' in q and not q_definition[1]:
                    q_definition[1] = q.replace('{D2}', '').replace('--', '')
                if '{Q1}' in q and not q_quality[0]:
                    q_quality[0] = q.replace('{Q1}', '').replace('--', '')
                if '{Q2}' in q and not q_quality[1]:
                    q_quality[1] = q.replace('{Q2}', '').replace('--', '')
                if '{P1}' in q and not q_policy[0]:
                    q_policy[0] = q.replace('{P1}', '').replace('--', '')
                if '{P2}' in q and not q_policy[1]:
                    q_policy[1] = q.replace('{P2}', '').replace('--', '')

        questions = {"fact": q_fact, "definition": q_definition, "quality": q_quality, "policy": q_policy}

        return questions
