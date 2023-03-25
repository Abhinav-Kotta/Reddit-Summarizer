import praw
import pandas as pd
 
reddit_read_only = praw.Reddit(client_id="vVsTe3SaUW3ERIf18O5Wew",         # your client id
                               client_secret="RbS0oC_yqN16XuZ0MoMCJxv8sLa7SA",      # your client secret
                               user_agent="Summarizer")        # your user agent
 
 
url = "https://www.reddit.com/r/ucf/comments/1218051/did_anyone_else_have_a_poor_experience_with_ucf/"
submission = reddit_read_only.submission(url=url)

from praw.models import MoreComments

post_comments = []
 
for comment in submission.comments:
    if type(comment) == MoreComments:
        continue
 
    post_comments.append(comment.body)
 
# creating a dataframe
comments_df = pd.DataFrame(post_comments, columns=['comment'])
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(comments_df)


