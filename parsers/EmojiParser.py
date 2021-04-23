from emoji import UNICODE_EMOJI


def fix_value(v):
    return v.replace(":", "").split("_")


EMOJI_DICT = {k: fix_value(v) for k, v in UNICODE_EMOJI.items()}


def parse_word(word):
    if word in EMOJI_DICT:
        return True, EMOJI_DICT[word]
    return False, []
