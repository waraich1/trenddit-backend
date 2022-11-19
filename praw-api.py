import praw
from os import environ



reddit = praw.Reddit(
    client_id=environ.get('CLIENT_ID'),
    client_secret=environ.get('SECRET_ID'),
    user_agent="Trenddit/0.0.2",
    refresh_token='2350269160941-tBMkp2mTTMS_UUidLWbSwazOXzP4CA',
    username=environ.get('USER_ID'),
    password=environ.get('PASSWORD'),
)



print(reddit.read_only)
reddit.read_only = True

subreddit = reddit.subreddit("redditdev")

print(subreddit.display_name)
# Output: redditdev
print(subreddit.title)
# Output: reddit development
# print(subreddit.description)

for submission in reddit.subreddit("canada").hot(limit=10):
    print(submission.title)