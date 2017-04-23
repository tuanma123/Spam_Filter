import math
import os

HAM_FOLDER = "data/train/ham"
SPAM_FOLDER = "data/train/spam"
TEST_DATE = "data/test"
HAM_COUNT = sum(os.path.isfile(os.path.join(HAM_FOLDER, f)) for f in os.listdir(HAM_FOLDER))
SPAM_COUNT = sum(os.path.isfile(os.path.join(SPAM_FOLDER, f)) for f in os.listdir(SPAM_FOLDER))


def token_set(filename):
    #open the file handle
    with open(filename, 'r') as f:
        #ignore the Subject beginning
        text = f.read()[9:]
        #put it all on one line
        text = text.replace('\r', '')
        text = text.replace('\n', ' ')
        #split by spaces
        tokens = text.split(' ')
        #return the set of unique tokens
        return set(tokens)


def word_count(file_path):
    """
    Maps the number of  unique times a word appears over a directory of text files. Max occurrence of one word per file.
    
    Goes through all files in a specified folder. Constructs the unique token set for each text file. 
    Then iterates through the tokens and check if an interger mapping already exists. If it does, then just increase
    the count by 1. Otherwise, set the count to 1.
    
    :param file_path: The relative directory path containing the email text files(the ham folder or the spam folder).
    
    :return: A map mapping string words to the number of unique times they have appeared across the directory of 
    text files. 
    """
    word_counts = {}

    # Iterate through the entire folder.
    for file in os.listdir(file_path):
        tokens = token_set(file_path + "/" + file)
        for token in tokens:
            if token in word_counts:
                word_counts[token] += 1
            else:
                word_counts[token] = 1
    return word_counts


def word_probability():
    """
    Calculates the probability of a word appearing in both a spam email and a ham email.
    
    Constructs the word map counting for both ham and spam emails. Then for each word in both of those word count maps, 
    creates a new map that maps each string to the total probability that it appears in its given type of email. That 
    probability is simply the integer value for each word from the original word map divided by the number of emails
    for the type.
    
    :return: Returns a tuple containing maps that map words to the probability that they appear in a specific of email.
    The format is the ham mapping at the 0th index, followed by the spam mapping at the 1st index.
    """
    # Get the word counts for both ham and spam
    ham_map = word_count(HAM_FOLDER)
    spam_map = word_count(SPAM_FOLDER)

    ham_map_probability = {}
    spam_map_probability = {}

    """ Iterate through both the ham key set and the spam key set. Add new entries for each key with the correct
    probability and Laplace smoothing. Check if the key exists in the other key set. If not, add it in to ensure that
    there are no 0 probabilities when calcutaing the total probality that an email is spam.

    Assertions: None of the words' probabilities should exceed 1 by the principles of statistics.
    """
    for key in ham_map.keys():
        # Insert a new entry containing the key with the a mapping to the correct probability and Laplace smoothing.
        ham_map_probability[key] = (ham_map[key] + 1) / (HAM_COUNT + 2)
        assert 0 < ham_map_probability[key] < 1
        # If the key is not in the spam key set, then add it with Laplace smoothing in order to avoid 0 probabilities.
        if key not in spam_map.keys():
            spam_map_probability[key] = 1 / (SPAM_COUNT + 2)
            assert 0 < spam_map_probability[key] < 1
    for key in spam_map.keys():
        # Insert a new entry containing the key with the a mapping to the correct probability and Laplace smoothing.
        spam_map_probability[key] = (spam_map[key] + 1) / (SPAM_COUNT + 2)
        assert 0 < spam_map_probability[key] < 1
        # If the key is not in the spam key set, then add it with Laplace smoothing in order to avoid 0 probabilities.
        if key not in ham_map.keys():
            ham_map_probability[key] = 1 / (HAM_COUNT + 2)
            assert 0 < ham_map_probability[key] < 1
    # Returns a tuple containing both value maps.
    return ham_map_probability, spam_map_probability


def label_spam(test_files):
    # Get the probabilities of words for the training set
    words_prob = word_probability()
    # Calculate the probability of ham and spam
    prob_spam = SPAM_COUNT / (HAM_COUNT + SPAM_COUNT)
    prob_ham = HAM_COUNT / (SPAM_COUNT + HAM_COUNT)
    assert 0 < prob_ham < 1
    assert 0 < prob_spam < 1
    # Get all the words that appear in both the ham and spam training data.
    word_set = word_count(HAM_FOLDER).keys() & word_count(SPAM_FOLDER).keys()

    for file in sorted(os.listdir(test_files)):
        # Get the tokens of the file
        tokens = token_set(test_files + "/" + file)
        # Iterate through the tokens from the test email
        prob_word_spam = 0
        prob_word_ham = 0
        for token in tokens:
            # Only process if the token is in either ham or spam(their union). Ignore, otherwise.
            if token in (word_set):
                prob_word_ham += math.log10(words_prob[0][token])
                prob_word_spam += math.log10(words_prob[1][token])
        # Calculate the probabilities using the formulas given.
        is_spam = prob_word_spam + math.log10(prob_spam) > prob_word_ham + math.log10(prob_ham)
        # Return whether the probability of it being spam is greater than 1/2. If so, it spam. It is ham otherwise.
        output = file
        output += " spam" if is_spam else " ham"
        print(output)

label_spam("data/test")