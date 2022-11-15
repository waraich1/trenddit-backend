import praw

# reddit = praw.Reddit(
#     client_id="_cYY9dLkaIUy6I-p_yzXgw",
#     client_secret="hO6SAqvDBRu7rIyei6C9uE-JscMPtA",
#     user_agent="Trenddit/0.0.1",
# )

reddit = praw.Reddit(
    client_id="_cYY9dLkaIUy6I-p_yzXgw",
    client_secret="hO6SAqvDBRu7rIyei6C9uE-JscMPtA",
    user_agent="Trenddit/0.0.2",
    refresh_token="2350269160941-a5OpOSu7rTd4TTVmIKDAtO2zQPcSag",
    password="Harkanwar@6762",
    username="trenddit-dev",
)

print(reddit.read_only)
reddit.read_only = True

subreddit = reddit.subreddit("redditdev")

print(subreddit.display_name)
# Output: redditdev
print(subreddit.title)
# Output: reddit development
print(subreddit.description)