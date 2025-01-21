import re  # Import the `re` module for working with regular expressions
import string  # Import `string` module to handle punctuation
import pymorphy2  # Import `pymorphy2` for morphological analysis (e.g., lemmatization)
from nltk.corpus import stopwords  # Import the `stopwords` list from NLTK
import nltk  # Import the NLTK library for natural language processing

def doc_mining(document_text):
    """
    Processes the given text document:
    - Removes punctuation, digits, and other unwanted characters.
    - Removes stop words.
    - Normalizes words to their base form using pymorphy2.
    """
    # Read the content of the document and convert it to lowercase
    text_string = document_text.read().lower()

    # Create a regex pattern to match and remove punctuation
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    out = regex.sub(' ', text_string)  # Replace punctuation with a space

    # Remove all digits from the text
    out = re.sub(r"\d+", "", out)

    # Remove single Cyrillic characters surrounded by spaces
    out = re.sub('(\\b[А-Яа-я] \\b|\\b [А-Яа-я]\\b)', '', out)

    # Remove single Latin characters surrounded by spaces
    out = re.sub('(\\b[A-Za-z] \\b|\\b [A-Za-z]\\b)', '', out)

    # Remove standalone Latin words
    out = re.sub(r"\b[a-z]+\b", '', out)

    # Remove words with mixed Latin and Cyrillic characters
    out = re.sub(r"\b[a-z]+[а-я]+\b", '', out)
    out = re.sub(r"\b[а-я]+[a-z]+[а-я]+\b", '', out)
    out = re.sub(r"\b[а-я]+[a-z]+\b", '', out)
    out = re.sub(r"\b[a-z]+[а-я]+[a-z]+\b", '', out)

    # Replace multiple spaces with a single space
    out = re.sub(r"[\s]+", ' ', out)

    # Remove stop words using NLTK's list of Russian stop words
    stopwords_nltk = stopwords.words("russian")  # Get the list of Russian stop words
    words = nltk.word_tokenize(out)  # Tokenize the cleaned text into words
    without_stop_words = [word for word in words if not word in stopwords_nltk]  # Filter out stop words

    # Normalize words to their base form using pymorphy2
    morph = pymorphy2.MorphAnalyzer()  # Create a morphological analyzer instance
    for i in range(len(without_stop_words)):
        p = morph.parse(without_stop_words[i])[0]  # Parse each word
        without_stop_words[i] = p.normal_form  # Replace the word with its base (normal) form

    # Join the normalized words back into a single string
    out2 = " ".join(str(x) for x in without_stop_words)

    # Return the processed text
    return out2
