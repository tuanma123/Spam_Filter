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
    folder = os.listdir(file_path)
    for file in folder:
        tokens = token_set(file_path + "/" + file)
        for token in tokens:
            if token in word_counts:
                word_counts[token] = word_counts[token] + 1
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
    ham_map = word_count(HAM_FOLDER)
    spam_map = word_count(SPAM_FOLDER)

    ham_map_probability = {}
    spam_map_probability = {}

    for key in ham_map.keys():
        ham_map_probability[key] = ham_map[key] / HAM_COUNT
    for key in spam_map.keys():
        spam_map_probability[key] = spam_map[key] / SPAM_COUNT
    return ham_map_probability, spam_map_probability


def label_spam(text_file):
    tokens = token_set(text_file)
    prob_spam = SPAM_COUNT / (HAM_COUNT + SPAM_COUNT)
    prob_ham = HAM_COUNT / (SPAM_COUNT + HAM_COUNT)
    word_probabilities = word_probability()
	


