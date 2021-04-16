"""Ensure that the functions in the nlp package are working correctly."""

from mesmsage import nlp


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
        "I'm going to be late to my shifts this week.",
        "I'm going to be late to my shift on Friday of this week.",
        "I'm going to be late to my shift on Friday.",
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


def test_create_default_intent_dictionary():
    """Ensure that it is possible to create the default intent dictionary."""
    default_intent_dictionary = nlp.create_default_intent_dictionary(intent_dictionary)
    assert default_intent_dictionary is not None
    for key, value in default_intent_dictionary["cats"].items():
        assert value == 0.0


def test_create_entire_jsonl_dictionary():
    """Ensure that it is possible to construct the entire dictionary in the JSONL format."""
    entire_jsonl_dictionary_list = (
        nlp.convert_dictionary_to_spacy_jsonl_dictionary_list(intent_dictionary)
    )
    assert entire_jsonl_dictionary_list is not None
    print(entire_jsonl_dictionary_list)
