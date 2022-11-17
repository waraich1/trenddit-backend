import praw
from os import environ

# reddit = praw.Reddit(
#     client_id="_cYY9dLkaIUy6I-p_yzXgw",
#     client_secret="hO6SAqvDBRu7rIyei6C9uE-JscMPtA",
#     user_agent="Trenddit/0.0.1",
# )

reddit = praw.Reddit(
    client_id=environ.get('Client_id'),
    client_secret=environ.get('seceret_id'),
    user_agent="Trenddit/0.0.2",
    refresh_token="2350269160941-a5OpOSu7rTd4TTVmIKDAtO2zQPcSag",
    password=environ.get('user_id'),
    username=environ.get('password'),
)

print(reddit.read_only)
reddit.read_only = True

subreddit = reddit.subreddit("redditdev")

print(subreddit.display_name)
# Output: redditdev
print(subreddit.title)
# Output: reddit development
print(subreddit.description)