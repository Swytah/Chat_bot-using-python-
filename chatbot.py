
!pip install numpy
!pip install nltk
!pip install scikit-learn
!pip install python-docx
!pip install PyPDF2

import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import random
import string

from docx import Document
import PyPDF2
import nltk
import string
import random
from google.colab import files  


def upload_file():
    print("Select the type of file you want to upload:")
    print("1. Text file (.txt)")
    print("2. PDF file (.pdf)")
    print("3. Word file (.docx)")
    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        print("Please upload your text file:")
        uploaded = files.upload()
        file_name = next(iter(uploaded))
        file_contents = open_file_and_read_contents(file_name)
        return file_contents, file_name

    elif choice == '2':
        print("Please upload your PDF file:")
        uploaded = files.upload()
        file_name = next(iter(uploaded))
        file_contents = read_pdf(file_name)
        return file_contents, file_name

    elif choice == '3':
        print("Please upload your Word file:")
        uploaded = files.upload()
        file_name = next(iter(uploaded))
        file_contents = read_word_file(file_name)
        return file_contents, file_name

    else:
        print("Invalid choice. Please select 1, 2, or 3.")
        return None, None

# Function to open and read text file
def open_file_and_read_contents(file_name):
    try:
        with open(file_name, 'r') as file:
            file_contents = file.read()
        return file_contents
    except FileNotFoundError:
        print("File not found or unable to open the file.")
        return None
    except IOError:
        print("An error occurred while reading the file.")
        return None

# Function to read PDF file
def read_pdf(file_name):
    try:
        with open(file_name, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            file_contents = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                file_contents += page.extract_text()
            return file_contents
    except Exception as e:
        print("Error:", e)
        return None

# Function to read Word file
def read_word_file(file_name):
    try:
        doc = Document(file_name)
        file_contents = ''
        for paragraph in doc.paragraphs:
            file_contents += paragraph.text + '\n'
        return file_contents
    except Exception as e:
        print("Error:", e)
        return None

# Test the function
file_contents, file_name = upload_file()

file_contents=file_contents.lower()

sent_tokens = nltk.sent_tokenize(file_contents)
word_tokens = nltk.word_tokenize(file_contents)

sent_tokens[:2]
word_tokens[:5]

sent_tokens[0]

word_tokens[:5]

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')

    tfidf = TfidfVec.fit_transform(sent_tokens)

    vals = cosine_similarity(tfidf[-1], tfidf)

    idx=vals.argsort()[0][-2]

    flat = vals.flatten()

    flat.sort()
    req_tfidf = flat[-2]

    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

def encode_sequence(tokenizer,length,lines):
    seq = tokenizer.texts_to_sequences(lines)
    seq = pad_sequences(seq, maxlen = length, padding='post')
    return seq

flag = True
print("ROBO: My name is VirBot.  If you want to exit, type Bye!")

if flag:
    y = input("Enter your interest: ")
    print("Enter your query related to", y)
    while flag:
        user_response = input()
        user_response = user_response.lower()

        if user_response != 'bye':
            if user_response == 'thanks' or user_response == 'thank you':
                flag = False
                print("ROBO: You are welcome..")
            else:
                if greeting(user_response) is not None:
                    print("ROBO: " + greeting(user_response))
                else:
                    print("ROBO: ", end="")
                    print(response(user_response))
                    sent_tokens.remove(user_response)
        else:
            flag = False
            print("ROBO: Bye! take care..")