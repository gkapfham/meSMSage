"""Use natural language processing (NLP) to determine intent and similarity in human responses."""

import operator

from multiprocessing import Pool

from typing import Dict
from typing import List

import en_core_web_lg

from mesmsage import configure

THRESHOLD = 0.85


# The dictionary of:
# {INTENT: [List of responses indicative of that intent]}
intent_dictionary = {
    "CANNOT": [
        "I cannot work my shift on Monday.",
        "Sorry, I can't work my shift on Monday.",
        "I regret that I cannot work my shift on Monday.",
        "I regret that I can't work my shift on Monday.",
        "I will no longer be able to work my shift on Monday.",
        "I have a schedule conflict and I cannot work my shift on Monday.",
        "I have a schedule conflict and I cannot work my shifts this week.",
        "Something came up and I cannot work my shifts this week.",
        "Something came up and I cannot work my shift on Monday.",
        "I'm too busy and I cannot work my shift on Monday.",
        "I'm too busy and I cannot work my shifts this week.",
    ],
    "CONFIRM": [
        "I can definitely work my assigned shifts, thanks for alerting me!",
        "I can work my shifts.",
        "I can work my shifts, thanks!",
        "I can work my shift on Monday.",
        "I can work my shifts this week.",
        "Yes, I can work all of my shifts this week.",
        "Sure, I can work my shifts on Monday.",
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
        "I think that there is a mistake in my shifts.",
        "I think that there are mistakes in my shifts. Are they correct?",
        "Are these shifts correct? I don't remember signing up for them!",
    ],
    "INQUIRE": [
        "Can you tell me who I am working with on Monday?",
        "Can you tell me who works with me on Monday?",
        "Who am I working with on Monday?",
        "Who works with me on Monday?",
        "Who am I working with this week?",
        "Who works with me this week?",
        "Can you tell me who works on my shifts this week?",
    ],
    "SICK": [
        "I do not feel good. I cannot work my shift today.",
        "I do not feel good. I cannot work my shifts next week.",
        "I do not feel good. I cannot work my shift today. Can you find a replacement?",
        "I do not feel good. I cannot work my shifts next week. Can you find a replacement?",
        "I feel sick. I cannot work my shift on Monday. Sorry!",
        "I am sick and cannot work my shift today. Can you find a replacement?",
        "I am ill and I cannot work my shifts next week.",
        "My child is sick and I cannot work my shifts next week.",
        "My child is sick and I cannot work my shifts next week. Can you help?",
        "My daughter is sick and I cannot work my shifts next week.",
        "My son is sick and I cannot work my shifts next week.",
        "My child is sick and I cannot work my shift on Monday.",
        "My daughter is sick and I cannot work my shift on Monday.",
        "My son is sick and I cannot work my shift on Monday.",
    ],
    "THANKS": [
        "Thanks for reminding me about my shifts, I appreciate it!",
        "Thank you for the reminder about my shifts!",
        "Thanks for reminding me about my shift on Monday!",
        "Thank you for reminder me about my shifts this week!",
        "I appreciate your reminder about my shifts, thanks!",
    ],
    "QUIT": [
        "I'm sorry but I no longer want to work at the Motzing Center.",
        "I'm sorry but I can no longer volunteer at the Motzing Center.",
        "I'm sorry but I no longer want to work at the Kovfino.",
        "I'm sorry but I can no longer volunteer at the Kovfino.",
        "I'm really sorry but I can no longer work at the Motzing Center.",
        "I'm really sorry but I can no longer work at Kovfino.",
    ],
}

response_dictionary = {
    "CANNOT": (
        "Thanks for letting us know that you cannot work one or more of your shifts."
        + " Jessica will contact you soon and also try to schedule a replacement! 🏃"
    ),
    "CONFIRM": (
        "Thanks for letting us know that you can work at least one of your shifts."
        + " We really appreciate your willingness to volunteer at the Motzing Center! 🤩"
    ),
    "FORGOT": (
        "Oh no! We are sorry to learn that you forgot one or more of your shifts."
        + " Jessica will contact you and try to schedule a replacement. 😉"
    ),
    "INCORRECT": (
        "We're sorry that there might be a misunderstanding about your shifts."
        + " Please check a previous text message to see what shifts we assigned to you."
        + " Jessica will contact you resolve any misunderstandings! 😬"
    ),
    "INQUIRE": (
        "Okay, it seems like you have a question about your shifts!"
        + " Please check a previous text message to see what shifts we assigned to you."
        + " Jessica will contact you to answer any other questions that you have. 😂"
    ),
    "SICK": (
        "Oh no, we're sorry to learn that you or someone you know might be sick!"
        + " We hope that you feel better soon."
        + " Jessica will attempt to reschedule your shifts. 🤒"
    ),
    "THANKS": (
        "Hey, thanks for letting us know that you appreciate the Motzing Center."
        + " We think that you are awesome, too!"
        + " Let Jessica know if you have ideas for improving this service, okay? 🤯"
    ),
    "QUIT": (
        "Uh oh, it sounds like volunteering at the Motzing Center might be causing you some trouble."
        + " We're sorry to hear about this and hope that we can improve the situation."
        + " Jessica will contact you in an attempt to address your concerns. 😢"
    ),
    "UNKNOWN": (
        "Sorry, we could not understand your message."
        + " I guess that is what happens when a program tries to understand a human!"
        + " Jessica will contact you to see if she can resolve this issue. 🤷"
    ),
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


def summarize_intent_scores(
    intent_scores_dictionary: Dict[str, List[float]]
) -> Dict[str, float]:
    """Summarize the intent scores down to the maximum number for each list of values."""
    intent_scores_summary_dictionary = {}
    for intent, scores_list in intent_scores_dictionary.items():
        intent_scores_summary_dictionary[intent] = max(scores_list)
    return intent_scores_summary_dictionary


def determine_intent(
    intent_scores_summary_dictionary: Dict[str, float]
) -> (str, float):
    """Determine the intent that best matches the one provided by the human user."""
    maximum_intent = max(
        intent_scores_summary_dictionary.items(), key=operator.itemgetter(1)
    )[0]
    return (maximum_intent, intent_scores_summary_dictionary[maximum_intent])


def create_response(
    summarized_intent_scores_dictionary: Dict[str, float],
    similarity_threshold=THRESHOLD,
) -> (str, str, float):
    """Create the response that should be the intended response for the human message."""
    global intent_responses
    (intent, score) = determine_intent(summarized_intent_scores_dictionary)
    message = None
    if score > similarity_threshold:
        message = response_dictionary[intent]
    else:
        message = response_dictionary["UNKNOWN"]
        intent = intent + " -> UNKNOWN" + f" because {score:0.4f} < {similarity_threshold}"
    return (message, intent, score)
