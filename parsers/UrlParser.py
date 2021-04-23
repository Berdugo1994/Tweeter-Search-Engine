import re
import urllib.parse as urlp


def url_func(sentence):
    """
    The function gets sentence - returns boolean result if contains urls, urls words splitted and the
    new string without the urls.
    :param sentence:
    """
    if 'http' in sentence:
        list_of_urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                  sentence)
        if len(list_of_urls) > 0:
            start_point = 0
            new_word = ''
            for url in list_of_urls:
                start_point_url = sentence.rfind(url)
                # -1 for not taking the white space
                new_word += sentence[:start_point_url - 1]
                sentence = sentence[start_point_url + len(url):]
            new_word += sentence
            urls_splitted = parse_urls(list_of_urls)
            return [True, urls_splitted, new_word]
    return [False]


def parse_urls(list_of_urls):
    """
    gets list of urls as full strings , splitted them and returns one list contains all parts of all urls.
    :param list_of_urls:
    :return:
    """
    url_words = []
    for word in list_of_urls:
        o = urlp.urlparse(word)
        if o.hostname == "t.co" or o.hostname == 't.' or o.hostname == "t":
            continue
        url_words += [o.scheme]

        if o.netloc[0:4] == 'www.':
            url_words += ([o.netloc[4:]])
        else:
            url_words.append(o.netloc)
        url_words += o.path.split('/')
        url_words += o.query.split('=')
        url_words += o.fragment
    str_list = list(filter(None, url_words))
    return str_list


def replace_short_to_long(fulltext, string_of_dic, indices, t_id):
    # Zogi will get the shorter, E-Zogi full text
    list_urls = string_of_dic.split('"')
    list_urls = [list_urls[i] for i in range(len(list_urls)) if i % 2 == 1]
    indices = (re.sub('|\]|\[', '', indices)).split(',')
    indices = [int(val) for val in indices]
    start_index = 0
    diff_chars = 0
    new_links = ""
    for i in range(1, len(list_urls), 2):
        clean_url = url_cleaner(list_urls[i])
        if clean_url is None:
            start_index += 2
            continue
        if fulltext[diff_chars + indices[start_index]:diff_chars + indices[start_index + 1]] == list_urls[i - 1]:
            new_links += " " + clean_url
            fulltext = fulltext[:int(indices[start_index]) + diff_chars] + fulltext[
                                                                           int(indices[start_index + 1]) + diff_chars:]
            diff_chars -= len(list_urls[i - 1])
        else:
            new_links += " " + list_urls[i]
            diff_chars -= len(list_urls[i])
        start_index += 2
    return new_links[1:] + " " + fulltext


def enlarge_full_text(string_of_dic):
    list_urls = string_of_dic[2:-2].split('"')
    new_urls = ""
    for i in range(2, len(list_urls), 2):
        new_urls += list_urls[i] + " "
    return new_urls


def url_cleaner(url):
    res = urlp.urlparse(url)
    if res[1] == 'twitter.com' or res[1] == 't.co':
        return None

    # not using the domain!
    relevant_string = res[2].split('/')
    clean_string = ""

    # This check is for sub string that has longer than 5 digits for example: eden.com/ *2020*/*5*/dad/*5151325151515*/
    for sub_str in relevant_string:
        if sub_str == '' or sub_str.isdigit() or sub_str == "post":
            continue
        clean_string += sub_str.replace("-", " ") + " "
    if clean_string == "":
        return None
    return clean_string
