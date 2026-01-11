import praw

reddit = praw.Reddit(
    client_id="my client id",
    client_secret="my client secret",
    user_agent="my user agent",
)

print(reddit.read_only)

for submission in reddit.subreddit("test").hot(limit=10):
    print(submission.title)