import math

notation_to_number = {
    "k": 1000,
    "m": 1000000,
    "b": 1000000000,
    "K": 1000,
    "M": 1000000,
    "B": 1000000000,
}

notation_signs_set = set(notation_to_number.keys())

number_notation_to_sign = {
    "thousand": 'K',
    "thousands": 'K',
    "million": 'M',
    "millions": 'M',
    "billion": 'B',
    "billions": 'B',
}


def is_number(s):
    if s == '':
        return False
    if s[0].islower() or s[0].isupper():
        return False
    s = s.replace(",", "")
    try:
        float(s)
        return True
    except ValueError:
        pass
    # try:
    #     unicodedata.numeric(s)
    #     return True
    except (TypeError, ValueError):
        pass
    return False


# def is_number(word):
#     if re.match(r'^-?\d+(?:\.\d+)?$', word.replace(",", "")) is None:
#         return False
#     return True


def is_number_notation(lower_word):
    return lower_word in number_notation_to_sign.keys()


def kmb_sign(lower_word):
    return number_notation_to_sign[lower_word]


def is_thousand_number(number):
    return 1000 <= number < 1000000


def is_million_number(number):
    return 1000000 <= number < 1000000000


def is_billion_number(number):
    return 1000000000 <= number < 1000000000000


def normalize_number(number):
    number = number.replace(",", "")
    if is_notation(number[-1]):
        f = float(number[:-1]) * notation_to_number[number[-1]]
    else:
        f = float(number)
    if is_thousand_number(f):
        number_normalize = round_down(f / 1000)
        return str(number_normalize) + "K"
    elif is_million_number(f):
        number_normalize = round_down(f / 1000000)
        return str(number_normalize) + "M"
    elif is_billion_number(f):
        number_normalize = round_down(f / 1000000000)
        return str(number_normalize) + "B"
    else:
        return number


def round_down(number):
    factor = 10 ** 3
    after_round = math.floor(number * factor) / factor
    if after_round.is_integer():
        return int(after_round)
    else:
        return after_round


def is_fraction(next_word):
    next_word_splitted = next_word.split('/')
    if len(next_word_splitted) != 2:
        return False
    for i in range(len(next_word_splitted)):
        if not is_number(next_word_splitted[i]):
            return False
    return True


def is_number_with_notation(word):
    return word[len(word) - 1] in notation_signs_set and is_number(word[:len(word) - 1])


def is_notation(notation):
    return notation in notation_signs_set


def to_numeric(word):
    word = word.replace(",", "")
    if word.isdigit() or is_number_with_notation(word):
        return word
    return str(float(word))


def is_percentage(lower_text):
    return lower_text in {'%', 'percent', 'percentage'}


# The tokenizer splits commas, we need to build back the long number.
# We dont keep build it if the next number is with - / +
# Also make sure if there is something like this: 0.5,0.3,0.2 we dont build it to long number
# If there is sign like k,m,b also add to number
def collect_trailing_number(i, text_tokens, word, text):
    i = i + 1

    is_last_number = is_number(word)
    while len(text_tokens) > i and ((not is_last_number and
                                     '+' not in text_tokens[i]
                                     and '-' not in text_tokens[i]
                                     and is_number(text_tokens[i])) or

                                    ('.' not in word
                                     and text_tokens[i] == ',') or

                                    (is_notation(text_tokens[i])) or

                                    # The tokenizer for some reason split '1000000000' to '10000000' and '00',
                                    # This is the fix
                                    (len(word) >= 8 and
                                     word in text and
                                     text.index(word) + len(word) < len(text) and
                                     text[text.index(word) + len(word)].isdigit() and
                                     is_number(text_tokens[i]))
    ):
        is_last_number = is_number(text_tokens[i])
        word += text_tokens[i]
        i = i + 1
        if is_notation(text_tokens[i - 1]):
            break

    return word, i - 1
