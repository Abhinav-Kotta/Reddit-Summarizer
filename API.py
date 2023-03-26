import praw
import pandas as pd
import nltk #Importing NLTK library in python
import string #For filtering out strings
import numpy as np
import networkx as nx
from nltk.corpus import stopwords #import stop words
from nltk.tokenize import sent_tokenize, word_tokenize #import tokenizations
from sklearn.metrics.pairwise import cosine_similarity #import needed for TextRank algo
from string import punctuation #Fort sorting out punctuations
nltk.download('punkt')
#Downloading and importing stopwords from nltk from the English langaugae
nltk.download('stopwords') 
nltk.download('averaged_perceptron_tagger') 


###----- Function that prints summary based on user selection -----###
def printSummary(submission, comments, int):
    if (int == 0):
        print("Submission Summary:\n" + submission)
    elif (int == 1):
        print("Comment Summary:\n" + comments)
    
    else:
        print("Submission Summary:\n" + submission)
        print("\nComment Summary:\n" + comments)


###----- Function to detect bot based on the subreddit and name -----###
def combine_sentences(summary_sentences):
    #Split the two sentences 
    sentences = sent_tokenize(summary_sentences)
    
    #Just in case we don't have two sentences; more of a safe gaurd
    if len(sentences) == 2:
        #Assign sentence 1 and sentence 2
        sentence1, sentence2 = sentences[0], sentences[1]

        # Tokenize the sentences
        tokens1 = word_tokenize(sentence1)
        tokens2 = word_tokenize(sentence2)

        # Identify the part of speech for each token
        tagged_tokens1 = nltk.pos_tag(tokens1)
        tagged_tokens2 = nltk.pos_tag(tokens2)

        ## Identify the subject and verb in each sentence
        subject1, verb1 = None, None
        subject2, verb2 = None, None

        for tag in tagged_tokens1:
            if tag[1].startswith('V'):
                verb1 = tag[0]
            elif tag[1].startswith('N'):
                subject1 = tag[0]

        for tag in tagged_tokens2:
            if tag[1].startswith('V'):
                verb2 = tag[0]
            elif tag[1].startswith('N'):
                subject2 = tag[0]

        # Combine the sentences by selecting the subject and verb from each sentence
        if subject1 and verb2:
            # Use the subject from sentence 1 and the verb and object from sentence 2
            object2 = re.sub(f'^{verb2}\s*', '', sentence2)
            return f"{subject1} {verb2} {object2}"
        elif subject2 and verb1:
            # Use the subject from sentence 2 and the verb and object from sentence 1
            object1 = re.sub(f'^{verb1}\s*', '', sentence1)
            return f"{subject2} {verb1} {object1}"
        else:
            return "Could not summarize"
    
    
###----- Function to detect bot based on the subreddit and name -----###
def detect_bot(name):
    #Check for common bot phrases or patterns
    common_bot_phrases = ["bot", "mod", "moderator", "auto"]
    
    #Loop all of our phrases and check to see if it's in the name
    for phrases in common_bot_phrases:
        if phrases in name.lower():
            return True
        
    #Passed all of our tests, return False
    return False

###----- Helper function for summarize, returns preprocess_text -----###
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words and token not in punctuation]
    return filtered_tokens

###----- Summarizes text by using the TextRank Algorithm -----###
def summarize_text(text, summary_length):
    """
    Preprocess the text by filtering out stop words and punctuations

    Tokenizes the text into sentences
        preprocess_text
        sent_tokenize
    
    Create a sentence embedding for each sentence using a bag-of-words representation

    Create a graph where each node is a sentence
        Edges between nodes are weighted by the cosine similarity between the sentence embeddings
    
    PageRank algorithm is applied to the graph and calculates the imortance score for each sentence

    Sentences are sorted by their importance Score and the top N (summary_length parameter) are selected to form the "summary"

    If there are no sentences, it returns "No comment"

    """
    # Preprocess the text data
    filtered_tokens = preprocess_text(text)
    # Tokenize the text data into sentences
    sentences = sent_tokenize(text)
    
    #For edge cases
    if not sentences:
        return "Could not summarize"
    # Create sentence embeddings using a pre-trained word embedding model like Word2Vec or GloVe
    # Here, we'll use a simple bag-of-words representation for each sentence
    sentence_vectors = []
    for sentence in sentences:
        sentence_tokens = preprocess_text(sentence)
        vector = np.zeros(len(filtered_tokens))
        for token in sentence_tokens:
            if token in filtered_tokens:
                vector[filtered_tokens.index(token)] += 1
        sentence_vectors.append(vector)
    # Create a graph representation of the sentences using cosine similarity as the edge weight
    sentence_similarity_graph = nx.Graph()
    num_sentences = len(sentences)
    for i in range(num_sentences):
        for j in range(i+1, num_sentences):
            similarity = cosine_similarity(sentence_vectors[i].reshape(1,-1), sentence_vectors[j].reshape(1,-1))[0][0]
            sentence_similarity_graph.add_edge(i, j, weight=similarity)
    # Apply the PageRank algorithm to the sentence graph to calculate the importance score for each sentence
    #Check for out of bound cases
    if sentence_similarity_graph.number_of_nodes() > 0:
        scores = nx.pagerank(sentence_similarity_graph)
        # Sort the sentences based on their importance scores and select the top N sentences to form the summary
        ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
        #Check for out of bound cases
        if len(ranked_sentences) >= summary_length:
            summary_sentences = [ranked_sentences[i][1] for i in range(summary_length)]
        else:
            summary_sentences = [ranked_sentences[i][1] for i in range(len(ranked_sentences))]
        summary = ' '.join(summary_sentences)
        return summary
    else:
        return ""

###----- Helper Function... removing stop words -----###
def filterWords(comment):
    
    stop_words = set(stopwords.words('english'))

    #Split up the words from the comment we passed in, store in filtered_words
    words = comment.split() #used local variable for readability
    filtered_words = []
    
    #Loop every word
    for word in words:
        #filter out any punctuation on the word
        word = word.translate(str.maketrans("", "", string.punctuation))

        #filters out stop_words
        if (word.casefold() not in stop_words):
            filtered_words.append(word)

    #Update the filter text and return it
    filtered_text = ' '.join(filtered_words)
    return(filtered_text)

reddit_read_only = praw.Reddit(client_id="vVsTe3SaUW3ERIf18O5Wew",         # your client id
                               client_secret="RbS0oC_yqN16XuZ0MoMCJxv8sLa7SA",      # your client secret
                               user_agent="Summarizer")        # your user agent
 
url = "https://www.reddit.com/r/ucf/comments/1218051/did_anyone_else_have_a_poor_experience_with_ucf/"
submission = reddit_read_only.submission(url=url)

"""
Give the user an option to summarize:
0: Submission
1: Comments
anything else: Both
"""

from praw.models import MoreComments
#Creating a string to conjoin all the comments together
conjoined_comments = ""
for comment in submission.comments:
    if type(comment) == MoreComments:
        continue
    
    #Check to see if the comment is from a bot; skip these to avoid skewing
    if (detect_bot(comment.author.name)):
        continue
    
    #Implement helper function to detect botnames and ignore them 
    conjoined_comments = conjoined_comments + comment.body + ". "


printSubmission = summarize_text(submission.selftext, 2)
printComments = summarize_text(conjoined_comments, 2)
userInput = 2 #both by default but we can update this later
printSummary(printSubmission, printComments, userInput)