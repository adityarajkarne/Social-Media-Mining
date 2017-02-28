import os


def argmax(sequence):
    """Return the index of the highest value in a list.

    This is a warmup exercise.

    Remember that Python uses zero-based numbering of indexes.

    Args:
        sequence (list): A list of numeric values.

    Returns:
        int: The index of the highest value in `sequence`.

    """
    # YOUR CODE HERE
    return sequence.index(max(sequence))



def tokenize(string, lowercase=False):
    """Extract words from a string containing English words.

    Handling of hyphenation, contractions, and numbers is left to your
    discretion.

    Tip: you may want to look into the `re` module.

    Args:
        string (str): A string containing English.
        lowercase (bool, optional): Convert words to lowercase.

    Returns:
        list: A list of words.

    """
    # YOUR CODE HERE

    if lowercase:
        string = string.lower()
    lst = string.split(" ")


    for i in range(len(lst)):
        for letter in lst[i]:
            if not letter.isalpha():
                lst[i]=lst[i].replace(letter,"")

    lst=[x for x in lst if x]

    return lst


def shared_words(text1, text2):
    """Identify shared words in two texts written in English.

    Your function must make use of the `tokenize` function above. You should
    considering using Python `set`s to solve the problem.

    Args:
        text1 (str): A string containing English.
        text2 (str): A string containing English.

    Returns:
        set: A set with words appearing in both `text1` and `text2`.

    """
    # YOUR CODE HERE


    return (set(tokenize(text1, True)).intersection(set(tokenize(text2, True))))





def shared_words_from_filenames(filename1, filename2):
    """Identify shared words in two texts stored on disk.

    Your function must make use of the `tokenize` function above. You should
    considering using Python `set`s to solve the problem.

    For each filename you will need to `open` file and read the file's
    contents.

    There are two sample text files in the `data/` directory which you can use
    to practice on.

    Args:
        filename1 (str): A string containing English.
        filename2 (str): A string containing English.

    Returns:
        set: A set with words appearing in both texts.

    """
    # YOUR CODE HERE

    content_1=" ".join([line for line in open(filename1,'r')])
    content_2 = " ".join([line for line in open(filename2, 'r')])

    return set(set(tokenize(content_1, True)).intersection(tokenize(content_2, True)))






def text2wordfreq(string, lowercase=False):
    """Calculate word frequencies for a text written in English.

    Handling of hyphenation and contractions is left to your discretion.

    Your function must make use of the `tokenize` function above.

    Args:
        string (str): A string containing English.
        lowercase (bool, optional): Convert words to lowercase before calculating their
            frequency.

    Returns:
        dict: A dictionary with words as keys and frequencies as values.

    """
    # YOUR CODE HERE
    dct={}

    for word in tokenize(string, lowercase):
        if word in dct:
            dct[word]+=1
        else:
            dct[word]=1

    return dct


def lexical_density(string):
    """Calculate the lexical density of a string containing English words.

    The lexical density of a sequence is defined to be the number of
    unique words divided by the number of total words. The lexical
    density of the sentence "The dog ate the hat." is 4/5.

    Ignore capitalization. For example, "The" should be counted as the same
    type as "the".

    This function should use the `text2wordfreq` function.

    Args:
        string (str): A string containing English.

    Returns:
        float: Lexical density.

    """

    d=text2wordfreq(string, True)
    return len(d)/sum(d.values())




def hashtags(string):
    """Extract hashtags from a string.

    For example, the string `"RT @HouseGOP: The #StateOfTheUnion is strong."`
    contains the hashtag `#StateOfTheUnion`.

    Args:
        string (str): A string containing English.

    Returns:
        list: A list, possibly empty, containing hashtags.

    """
    # YOUR CODE HERE
    return [word for word in string.split(" ") if word[0] == "#"]


def jaccard_similarity(text1, text2):
    """Calculate Jaccard Similarity between two texts.

    The Jaccard similarity (coefficient) or Jaccard index is defined to be the
    ratio between the size of the intersection between two sets and the size of
    the union between two sets. In this case, the two sets we consider are the
    set of words extracted from `text1` and `text2` respectively.

    This function should ignore capitalization. A word with a capital
    letter should be treated the same as a word without a capital letter.

    Args:
        text1 (str): A string containing English words.
        text2 (str): A string containing English words.

    Returns:
        float: Jaccard similarity

    """
    # YOUR CODE HERE


    t1 = set(tokenize(text1, True))
    t2 = set(tokenize(text2, True))

    return len(t1.intersection(t2))/len(t1.union(t2))



