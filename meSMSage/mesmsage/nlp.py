"""Use natural language processing (NLP) to determine intent and similarity in human responses."""

import en_core_web_lg

from multiprocessing import Pool

from typing import Dict
from typing import List

from mesmsage import configure
from mesmsage import timer


# The dictionary of:
# {INTENT: [List of responses indicative of that intent]}
intent_dictionary = {
    "CANNOT": [
        "I cannot work my shift on Monday.",
        "Sorry, I can't work my shift on Monday.",
        "I regret that I cannot work my shift on Monday.",
        "I regret that I can't work my shift on Monday.",
        "I will no longer be able to work my shift on Monday.",
    ],
    "HELP": [
        "Can you help me to reschedule my shifts on Monday?",
        "Can you please reschedule my Monday shift to a different day?",
        "Can you please pick a replacement for my shift on Monday?",
        "Can you help me to pick new shifts?",
        "Can you clarify the date and time of my shifts this week?",
    ],
    "FORGOT": [
        "I forgot that I was supposed to work today. Can you find someone else?",
        "I forgot that my shift is today! I don't think I can make it now.",
        "I did not remember that I cannot work today. Can you find someone else?",
        "I forgot that I was supposed to work on Monday. Can someone cover my shift?",
        "I forgot that I cannot work on Monday. Can you schedule someone else please?",
    ],
    "INCORRECT": [
        "I don't think that I signed up for a shift on Monday.",
        "I did not sign up for a shift on Monday.",
        "I did not sign up for a shift today.",
        "I am not supposed to work on Monday. Is this correct?",
        "I don't remember agreeing to work a shift on Monday.",
    ],
    "INQUIRE": [
        "Can you tell me who I am working with on Monday?",
        "Can you tell me who works with me on Monday?",
        "Who am I working with on Monday?",
        "Who works with me on Monday?",
        "Can you tell me who works on my shifts this week?",
    ],
    "SICK": [
        "I do not feel good. I cannot work my shift today.",
        "I do not feel good. I cannot work my shifts next week.",
        "I feel sick. I cannot work my shift on Monday. Sorry!",
        "I am sick and cannot work my shift today.",
        "I am sick and I cannot work my shifts next week.",
    ],
    "THANKS": [
        "Thanks for reminding me about my shifts, I appreciate it!",
        "Thank you for the reminder about my shifts!",
        "Thanks for reminding me about my shift on Monday!",
        "Thank you for reminder me about my shifts this week!",
        "I appreciate your reminder about my shifts, thanks!"
    ],
    "QUIT": [
        "I'm sorry but I no longer want to work at the Motzing Center.",
        "I'm too busy and I can no longer volunteer at the Motzing Center.",
        "I'm really sorry but I can no longer work at Kovfino.",
        "I cannot work my shift on Monday.",
        "I cannot work any of my shifts right now.",
    ],
}

# globally load the spaCy NLP model to
# avoid the costs of repeated loading
spacy_nlp = en_core_web_lg.load()


def calculate_similarity(candidate_response: str, human_response: str) -> float:
    """Calculate the similarity between a candidate response and a specific human response."""
    # extract a logger
    logger = configure.configure_logging()
    global spacy_nlp
    human_response_nlp = spacy_nlp(human_response)
    candidate_response_nlp = spacy_nlp(candidate_response)
    similarity = human_response_nlp.similarity(candidate_response_nlp)
    logger.debug(f"Calculate the similarity as: {similarity}")
    return similarity


def calculate_similarities(
    candidate_responses: List[str], human_response: str, parallel: bool = True
) -> List[float]:
    """Calculate the similarities between the candidate responses and the human response."""
    score_list = []
    if parallel:
        print("Running in parallel")
        pool = Pool()
        response_iterable = []
        for response in candidate_responses:
            response_iterable.append((response, human_response))
        score_list = pool.starmap(calculate_similarity, response_iterable)
    else:
        print("Running sequentially")
        for candidate_response in candidate_responses:
            current_response_score = calculate_similarity(
                candidate_response, human_response
            )
            score_list.append(current_response_score)
    return score_list


def calculate_intent_scores(
    human_response: str, parallel: bool = True
) -> Dict[str, List[float]]:
    """Determine the intent of the candidate response using the global intent_dictionary."""
    global intent_dictionary
    # extract a logger
    logger = configure.configure_logging()
    logger.debug(intent_dictionary)
    # create the dictionary of the intents and the scores
    intent_scores_dictionary = {}
    # calculate the similarity scores between the candidate responses in the
    # intent dictionary and the actual response from the human
    for intent, response_list in intent_dictionary.items():
        score_list = calculate_similarities(response_list, human_response, parallel)
        intent_scores_dictionary[intent] = score_list
    # return the dictionary of the form:
    # {The intent (e.g., "SICK"): [List of float scores for each candidate response]}
    return intent_scores_dictionary
