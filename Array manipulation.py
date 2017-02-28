
import os
import string
import re
import numpy as np


def load_nytimes_document_term_matrix_and_labels():
    """Load New York Times art and music articles.

    Articles are stored in a document-term matrix.

    Returns:
        (array, list): A document term matrix (as a Numpy array) and a list of labels.
    """
    import pandas as pd
    nytimes = pd.read_csv(os.path.join('data', 'nytimes-art-music-simple.csv'), index_col=0)
    labels = [document_name.rstrip(string.digits) for document_name in nytimes.index]
    return nytimes.values, labels


def normalize_document_term_matrix(document_term_matrix):
    """Normalize a document-term matrix by length.

    Each row in `document_term_matrix` is a vector of counts. Divide each
    vector by its length. Length, in this context, is just the sum of the
    counts or the Manhattan norm.

    For example, a single vector $(0, 1, 0, 1)$ normalized by length is $(0,
    0.5, 0, 0.5)$.

    Args:
        document_term_matrix (array): A document-term matrix of counts

    Returns:
        array: A length-normalized document-term matrix of counts

    """
    document_term_matrix, labels = load_nytimes_document_term_matrix_and_labels()

    document_term_matrix = document_term_matrix.astype(np.float64)
    for i in range(len(document_term_matrix)):
        document_term_matrix[i] = document_term_matrix[i] / sum(document_term_matrix[i])
    return document_term_matrix



def distance_matrix(document_term_matrix):
    """Calculate a NxN distance matrix given a document-term matrix with N rows.

    Each row in `document_term_matrix` is a vector of counts. Calculate the
    Euclidean distance between each pair of rows.

    Args:
        document_term_matrix (array): A document-term matrix of counts

    Returns:
        array: A square matrix of distances.

    """
    trix = np.empty([document_term_matrix.shape[0], document_term_matrix.shape[0]], dtype=float)

    for i in np.arange(len(document_term_matrix)):
        x = document_term_matrix[i]
        for j in np.arange(len(document_term_matrix)):
            y = document_term_matrix[j]
            trix[i, j] = np.linalg.norm(x - y)
    return trix



def jaccard_similarity_matrix(document_term_matrix):
    """Calculate a NxN similarity matrix given a document-term matrix with N rows.

    Each row in `document_term_matrix` is a vector of counts. Calculate the
    Jaccard similarity between each pair of rows.

    Tip: you are working with an array not a list of words or a dictionary of
    word frequencies. While you are free to convert the rows back into
    pseudo-word lists or dictionary of pseudo-word frequencies, you may wish to
    look at the functions ``numpy.logical_and`` and ``numpy.logical_or``.

    Args:
        document_term_matrix (array): A document-term matrix of counts

    Returns:
        array: A square matrix of similarities.

    """
    trix = np.empty([document_term_matrix.shape[0], document_term_matrix.shape[0]], dtype=float)

    for i in np.arange(len(document_term_matrix)):
        x = document_term_matrix[i]
        for j in np.arange(len(document_term_matrix)):
            y = document_term_matrix[j]
            inter=np.logical_and(x,y)
            uni=np.logical_or(x,y)
            trix[i, j] = inter[inter==True].shape[0]/uni[uni==True].shape[0]
    return trix



def nearest_neighbors_classifier(new_vector, document_term_matrix, labels):
    """Return a predicted label for `new_vector`.

    You may use either Euclidean distance or Jaccard similarity.

    Args:
        new_vector (array): A vector of length V
        document_term_matrix (array): An array with shape (N, V)
        labels (list of str): List of N labels for the rows of `document_term_matrix`.

    Returns:
        str: Label predicted by the nearest neighbor classifier.

    """
    # YOUR CODE HERE
    tracker = np.array([])
    for i in range(document_term_matrix.shape[0]):
        tracker=np.append(tracker, np.linalg.norm(document_term_matrix[i]-new_vector))
    return labels[np.argmin(tracker)]



def extract_hashtags(tweet):
    """Extract hashtags from a string.

    For example, the string `"RT @HouseGOP: The #StateOfTheUnion is strong."`
    contains the hashtag `#StateOfTheUnion`.

    The method used here needs to be robust. For example, the following tweet does
    not contain a hashtag: "This tweet contains a # but not a hashtag."

    Args:
        tweet (str): A tweet in English.

    Returns:
        list: A list, possibly empty, containing hashtags.

    """
    return re.findall('#[\w]+', tweet)


def extract_mentions(tweet):
    """Extract @mentions from a string.

    For example, the string `"RT @HouseGOP: The #StateOfTheUnion is strong."`
    contains the mention ``@HouseGOP``.

    The method used here needs to be robust. For example, the following tweet
    does not contain an @mention: "This tweet contains an email address,
    user@example.net."

    Args:
        tweet (str): A tweet in English.

    Returns:
        list: A list, possibly empty, containing @mentions.

    """
    userLst = re.findall("(^|[^@\w])@(\w{1,15})", tweet)
    final = ["@" + t[1] for t in userLst]
    return final


def adjacency_matrix_from_edges(pairs):
    """Construct and adjacency matrix from a list of edges.

    An adjacency matrix is a square matrix which records edges between vertices.

    This function turns a list of edges, represented using pairs of comparable
    elements (e.g., strings, integers), into a square adjacency matrix.

    For example, the list of pairs ``[('a', 'b'), ('b', 'c')]`` defines a tree
    with root node 'b' which may be represented by the adjacency matrix:

    ```
    [[0, 1, 0],
     [1, 0, 1],
     [0, 1, 0]]
    ```

    where rows and columns correspond to the vertices ``['a', 'b', 'c']``.

    Vertices should be ordered using the usual Python sorting functions. That
    is vertices with string names should be alphabetically ordered and vertices
    with numeric identifiers should be sorted in ascending order.

    Args:
        pairs (list of [int] or list of [str]): Pairs of edges

    Returns:
        (array, list): Adjacency matrix and list of vertices. Note
            that this function returns *two* separate values, a Numpy
            array and a list.

    """
    # YOUR CODE HERE
    lst = []
    for tple in pairs:
        for entity in tple:
            if entity not in lst:
                lst.append(entity)
    lst.sort()

    trix = np.zeros([len(lst), len(lst)], dtype=int)
    for pair in pairs:
        trix[lst.index(pair[0]), lst.index(pair[1])] = 1
        trix[lst.index(pair[1]), lst.index(pair[0])] = 1
    return trix,lst



def mentions_adjacency_matrix(list_of_mentions):
    """Construct an adjacency matrix given lists of mentions.

    Given the following list of mentions:

    - [@nytimes]
    - [@nytimes, @washtimes]
    - [@foxandfriends]
    - [@nytimes]
    - [@washtimes, @foxandfriends]

    One would expect as a result the following adjacency matrix:

      [[ 0.,  1.,  0.,  1.,  0.],
       [ 1.,  0.,  0.,  1.,  1.],
       [ 0.,  0.,  0.,  0.,  1.],
       [ 1.,  1.,  0.,  0.,  0.],
       [ 0.,  1.,  1.,  0.,  0.]]

    Where we can see, for example, that the third node is connected to the
    fifth node (because both mention ``@foxandfriends``).

    Args:
        list_of_mentions (list of list of str): List of mentions

    Returns:
        array: An adjacency matrix.

    """
    # YOUR CODE HERE

    trix = np.zeros([len(list_of_mentions), len(list_of_mentions)], dtype=int)
    for i in range(len(list_of_mentions)):
        for word in list_of_mentions[i]:
            z = [word in list_of_mentions[j] for j in range(len(list_of_mentions))]

            for m in range(len(z)):
                if m != i and z[m]:
                    trix[i, m] = 1
    return trix


