import praw

#Needed API
reddit = praw.Reddit(
    client_id="XMGj2fmcs5FgUYhYGk-byw",
    client_secret="9IVflk-xYK2j8XmKm993aTT1eE35ew",
    user_agent="Summarizer",
)

subreddit = reddit.subreddit('all')
top_posts = subreddit.hot(limit=10)

for post in top_posts:
    print(post.title)