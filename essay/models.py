import datetime

from django.db import models
from django.utils import timezone
from random import *


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
            e = "Because of %s, %s" % (fact2, fact1)
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
    questions = {
        "fact": ["What is the problem?",
                 "How did it begin and what are the causes?",
                 ],
        "definition": ["To what larger class of things does it belong?",
                       "What are its parts, and how are they related?",
                       ],
        "quality": ["What is the damage of this problem?",
                    "Is there positive impact of this issue?",
                    ],
        "policy": ["Opinion about this issue?",
                   "Who disagrees with you?"],
    }

    def __init__(self, topic):
        self.topic = topic

    def get_questions(self):
        return self.questions
