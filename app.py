from flask import Flask, jsonify
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
    # Preprocess the text data
    filtered_tokens = preprocess_text(text)
    # Tokenize the text data into sentences
    sentences = sent_tokenize(text)
    
    #For edge cases
    if not sentences:
        return ""
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

app = Flask(__name__)

reddit_read_only = praw.Reddit(client_id="vVsTe3SaUW3ERIf18O5Wew",         # your client id
                               client_secret="RbS0oC_yqN16XuZ0MoMCJxv8sLa7SA",      # your client secret
                               user_agent="Summarizer")        # your user agent
 

@app.route('/')
def hello():
    return '<h1>Hello, app.py</h1>'

@app.route('/comments')
def get_reddit_comments():
    
    url = "https://www.reddit.com/r/buildapcsales/comments/121zxi1/gpu_asrock_radeon_rx_6800_xt_phantom_gaming/"
    submission = reddit_read_only.submission(url=url)

    from praw.models import MoreComments

    #Creating array for post comments and filteretedComments
    filtered_comments = []
    post_comments = []
    conjoined_comments = ""
 
    for comment in submission.comments:
        if type(comment) == MoreComments:
            continue
    
        #Check to see if the comment is from a bot; skip these to avoid skewing
        if (detect_bot(comment.author.name)):
            continue
    
        #Implement helper function to detect botnames and ignore them 
        conjoined_comments = conjoined_comments + comment.body + ". "
 
    # creating a dataframe
    comments_df = pd.DataFrame(filtered_comments, columns=['comment'])
    result = summarize_text(conjoined_comments, 3)

    return '<h1>{}</h1>'.format(result)