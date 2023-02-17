from ast import Return
from itertools import tee
from flask import redirect
import asyncpraw
import praw
from os import environ
from praw.models import MoreComments
import asyncio
import httpx
from datetime import datetime
from collections import Counter
import re
import spacy
import en_core_web_sm
import json
from aiohttp import ClientSession
import itertools
import requests


class AuthorF:
    def __init__(self, token) -> None:

        self.reddit = asyncpraw.Reddit(
            client_id=environ.get("CLIENT_ID"),
            client_secret=environ.get("SECRET_ID"),
            user_agent="Trenddit/0.0.2",
            refresh_token="2350269160941-qXus-QHk_R1RP3eIRF9mkOCHW3K6zQ",
            username=environ.get("USER_ID"),
            password=environ.get("PASSWORD"),
        )

        self.token = token
        self.reddit.read_only = True
        self.session = ClientSession()

    def __aiter__(self):
        return self.__wrapped__.__aiter__()

    async def get_author_details(self, username):
        user = await self.reddit.redditor(username, fetch=True)
        auth = requests.auth.HTTPBasicAuth(
            environ.get("CLIENT_ID"), environ.get("SECRET_ID")
        )
        # here we pass our login method (password), username, and password
        data = {
            "grant_type": "password",
            "username": environ.get("USER_ID"),
            "password": environ.get("PASSWORD"),
        }
        # setup our header info, which gives reddit a brief description of our app
        headers = {"User-Agent": "Trenddit/0.0.2"}
        name = user.name
        created = user.created_utc
        comment_karma = user.comment_karma
        post_karma = user.link_karma
        least_popular_post = {"score": float("inf")}
        most_popular_post = {"score": float("-inf")}
        least_popular_comment = {"score": float("inf")}
        most_popular_comment = {"score": float("-inf")}
        total_karma_req = requests.get(
            f"https://www.reddit.com/user/username/about.json",
            auth=auth,
            headers=headers,
            data=data,
        )
        res = total_karma_req.json()
        total_karma = res["data"]["total_karma"]

        submissions = user.submissions.new(limit=None)
        comments = user.comments.new(limit=None)
        post_details = dict()
        comment_details = dict()
        total_comments = 0
        total_posts = 0
        average_karma_comment = 0
        average_karma_post = 0

        async for link in submissions:
            post = {
                "subreddit": str(link.subreddit),
                "score": link.score,
                "num_comments": link.num_comments,
                "title": link.title,
            }

            if link.score < least_popular_post["score"]:
                least_popular_post = post

            if link.score > most_popular_post["score"]:
                most_popular_post = post

            if str(link.subreddit) not in post_details:
                post_details[str(link.subreddit)] = dict()
                # post_details[str(link.subreddit)]["posts"] = []
                post_details[str(link.subreddit)]["score"] = 0
                post_details[str(link.subreddit)]["num_of_posts"] = 0

            # post_details[str(link.subreddit)]["posts"].append(post)
            post_details[str(link.subreddit)]["score"] += link.score
            post_details[str(link.subreddit)]["num_of_posts"] += 1
            total_posts = total_posts + 1

        if least_popular_post["score"] == float("inf"):
            least_popular_post["score"] = 0

        if most_popular_post["score"] == float("-inf"):
            most_popular_post["score"] = 0

        async for comment in comments:
            comment_detail = {
                "subreddit": str(comment.subreddit),
                "score": comment.score,
                "body": comment.body,
            }

            if comment.score < least_popular_comment["score"]:
                least_popular_comment = comment_detail

            if comment.score > most_popular_comment["score"]:
                most_popular_comment = comment_detail

            if str(comment.subreddit) not in comment_details:
                comment_details[str(comment.subreddit)] = dict()
                # comment_details[str(comment.subreddit)]["comment"] = []
                comment_details[str(comment.subreddit)]["score"] = 0
                comment_details[str(comment.subreddit)]["num_of_comments"] = 0

            # comment_details[str(comment.subreddit)]["comment"].append(comment_detail)
            comment_details[str(comment.subreddit)]["score"] += comment.score
            comment_details[str(comment.subreddit)]["num_of_comments"] += 1
            total_comments = total_comments + 1

            if total_posts > 0:
                average_karma_post = post_karma / total_posts

            if total_comments > 0:
                average_karma_comment = comment_karma / total_comments

        if least_popular_comment["score"] == float("inf"):
            least_popular_comment["score"] = 0

        if most_popular_comment["score"] == float("-inf"):
            most_popular_comment["score"] = 0

        await self.session.close()
        await self.reddit.close()

        return {
            "name": name,
            "cake_day": created,
            "posts": post_details,
            "comments": comment_details,
            "total_posts": total_posts,
            "total_comments": total_comments,
            "comment_karma": comment_karma,
            "post_karma": post_karma,
            "least_popular_post": least_popular_post,
            "most_popular_post": most_popular_post,
            "least_popular_comment": least_popular_comment,
            "most_popular_comment": most_popular_comment,
            "average_karma_post": average_karma_post,
            "average_karma_comment": average_karma_comment,
            "total_karma": total_karma,
        }
