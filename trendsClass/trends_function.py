from turtle import pos
from flask import redirect
import praw
from os import environ
from praw.models import MoreComments
import datetime as dt  # library for date management
import json


class TrendsF:
    def __init__(self, token) -> None:

        self.reddit = praw.Reddit(
            client_id=environ.get("CLIENT_ID"),
            client_secret=environ.get("SECRET_ID"),
            user_agent="Trenddit/0.0.2",
            refresh_token=token,
            username=environ.get("USER_ID"),
            password=environ.get("PASSWORD"),
        )

        self.reddit.read_only = True

    def get_trend_posts(self, subreddit, query):
        list = []
        for submission in self.reddit.subreddit(subreddit).search(
            query, sort="top", time_filter="month"
        ):

            res_object = {
                "author": str(submission.author),
                "created_utc": submission.created_utc,
                "id": submission.id,
                "name": submission.name,
                "over_18": submission.over_18,
                "num_commenta": submission.num_comments,
                "upvote_ratio": submission.upvote_ratio,
            }
            list.append((res_object))
        return list
