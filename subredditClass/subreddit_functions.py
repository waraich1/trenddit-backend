from flask import redirect
import praw
from os import environ
from praw.models import MoreComments
import subredditClass.comment as comment


class SubredditF:
    def __init__(self, token) -> None:

        self.reddit = praw.Reddit(
            client_id=environ.get("CLIENT_ID"),
            client_secret=environ.get("SECRET_ID"),
            user_agent="Trenddit/0.0.2",
            refresh_token=token,
            username=environ.get("USER_ID"),
            password=environ.get("PASSWORD"),
        )
        self.token = token
        self.reddit.read_only = True

    def get_hot_posts(self, subredditName, num):
        res = []
        subreddit = self.reddit.subreddit(subredditName)
        for submission in subreddit.hot(limit=num):
            res.append(submission.title)
        return res

    def get_hot_comments(self, subredditName, num):
        res = []
        uuids = []
        subreddit = self.reddit.subreddit(subredditName)
        for submission in subreddit.hot(limit=num):
            post_comment = comment.get_comment(submission.id, "hot", False, self.token)
            res.extend(post_comment)
        return res
