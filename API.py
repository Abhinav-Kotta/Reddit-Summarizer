import praw
import pandas as pd
import nltk #Importing NLTK library in python
import string #For filtering out strings

#Helper Function... removing stop words
def filterWords(comment):
    #Downloading and importing stopwords from nltk from the English langaugae
    nltk.download('stopwords') 
    from nltk.corpus import stopwords 
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
        

    filtered_text = ' '.join(filtered_words)

    return(filtered_text)

 
reddit_read_only = praw.Reddit(client_id="vVsTe3SaUW3ERIf18O5Wew",         # your client id
                               client_secret="RbS0oC_yqN16XuZ0MoMCJxv8sLa7SA",      # your client secret
                               user_agent="Summarizer")        # your user agent
 
 
url = "https://www.reddit.com/r/ucf/comments/1218051/did_anyone_else_have_a_poor_experience_with_ucf/"
submission = reddit_read_only.submission(url=url)

from praw.models import MoreComments

#Creating array for post comments and filteretedComments
filtered_comments = []
post_comments = []
 
for comment in submission.comments:
    if type(comment) == MoreComments:
        continue
    
    filtered_comments.append(filterWords(comment.body))
 
# creating a dataframe
comments_df = pd.DataFrame(filtered_comments, columns=['comment'])

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(comments_df)
    