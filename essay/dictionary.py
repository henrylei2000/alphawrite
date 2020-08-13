class Question:
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

    dict = {'Observation': [
        "{F}How did it begin and what are the causes?",
        "{F}What happened to {ENTS}?",
        "{F}What is the story behind {ENTS}?",
        "{F}What do we know about \"{SUBJ}\"?",
        "{F}What happened to \"{SUBJ}\"?",
        "{F}What do we know about {SUBJ} and {OBJ}?",
        "{F}Any knowledge about \"{SUBJ}\" and \"{OBJ}\"?",
    ],
        'Nature': [
            "{D}What are its parts, and how are they related?",
            "{D}What is the nature of \"{SUBJ}\"?",
            "{D}What are the components of \"{SUBJ}?\"",
            "{D}What are the attributes of \"{OBJ}\"?",
            "{D}What are similar concepts to \"{OBJ}\"?",
            "{D}How are \"{SUBJ}\" and \"{OBJ}\" related?",
            "{D}What are similar concepts to \"{SUBJ}\" and \"{OBJ}\"?",
        ],
        'Evaluation': [
            "{Q1}Is it good or bad?",
            "{Q1}Is \"{SUBJ}\" positive or negative?",
            "{Q1}What role does \"{OBJ}\" serve?",
            "{Q1}Opinion about \"{OBJ}\" in the topic?",
        ],
        'Complication': [
            "{Q2}What would be a different evaluation on \"{SUBJ}\"?",
            "{Q2}What if we measure \"{SUBJ}\" differently?",
            "{Q2}Any different measurement about \"{OBJ}\"?",
        ],
        'Policy': [
            "{P}With previous ideas, what do you want to advocate?",
            "{P}Suggestion about \"{SUBJ}\" and \"{OBJ}\"?",
            "{P}What do you want to advocate about the \"{SUBJ}\"?",
        ]
            }
