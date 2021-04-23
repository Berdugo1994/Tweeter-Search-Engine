def parse_hashtag(word):
    """
        This function takes a hashtag word and create all the relevant subwords of it
        split words by '_' or by switch from lower to upper , using xor func (isupper of i and of i-1)..
        :param word: the hashtag without the prefix of #
        :return: list of subwords
        example : word =#StayAtHome || #stay_at_home -> {stay, at, home, #stayathome}
    """
    start_of_word = 0
    all_words = []
    num_of_words = 0
    all_words.append(word.replace('_', '').lower())
    word = word[1:]

    for i in range(1, len(word)):
        if not word[i].islower() and word[i] != '_':
            if not word[i - 1].isupper():
                all_words.append(word[start_of_word:i].lower())
                start_of_word = i
                num_of_words += 1
            elif len(word) > i + 1 and not word[i + 1].isupper():
                all_words.append(word[start_of_word:i + 1].lower())
                start_of_word = i + 1
                i += 1

        elif word[i] == '_':
            all_words.append(word[start_of_word:i].lower())
            start_of_word = i + 1
    if start_of_word is not len(word):
        num_of_words += 1
        all_words.append(word[start_of_word:len(word)].lower())

    # PullTest
    return [word for word in all_words if word != ''], num_of_words
