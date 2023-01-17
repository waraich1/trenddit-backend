from ast import Return
from flask import redirect
import praw
from os import environ
from praw.models import MoreComments
import asyncio
import httpx
from datetime import datetime
from collections import Counter


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
        result = []
        subreddit = self.reddit.subreddit("canada")
        for submission in subreddit.hot(limit=num):
            date = self.get_date(submission.created_utc)
            res.append({
                "title": submission.title,
                "date": str(date.day) + "/" + str(date.month) + "/" + str(date.year),
                "author": str(submission.author),
                "nsfw": submission.over_18,
                "upvote_ratio": submission.upvote_ratio

            })
            # res.append(submission.title)
        
        date_counter = Counter(item["date"] for item in res)
        result.append({"date-freq" : dict(date_counter)})
        authour_counter = Counter(item["author"] for item in res)
        result.append({"auth-freq" : dict(authour_counter)})
        nsfw_counter = Counter(item["nsfw"] for item in res)
        result.append({"nsfw-freq" : dict(nsfw_counter)})
        upvote_counter = Counter(item["upvote_ratio"] for item in res)
        result.append({"upvote-freq" : dict(upvote_counter)})
        return result

    def get_hot_comments(self, subredditName, num):
        res = []
        uuids = []
        subreddit = self.reddit.subreddit(subredditName)
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        }

        res = []
        uuids = []
        subreddit = self.reddit.subreddit("Canada")
        for submission in subreddit.hot(limit=50):
            url = self.make_url(submission.id, "hot", False)
            res.append(url)

        async def do_tasks():
            async with httpx.AsyncClient() as client:
                tasks = [client.get(url, headers=headers,
                                    follow_redirects=True) for url in res]
                result = await asyncio.gather(*tasks)
                return result
        res = asyncio.run(do_tasks())
# print(res)

        return self.convert_hot_comment_result(res)

    def make_url(self, id, sort, threaded):
        return f"http://oauth.reddit.com/comments/{id}?sort={sort}&threaded={threaded}"

    def convert_hot_comment_result(self, res):
        result = []

        for i in res:
            data = i.json()
            res = data[1]["data"]["children"]
            comment = data[1]["data"]["children"]
            for i in range(len(comment)):
                if "body" in comment[i]["data"] and comment[i]["data"]["body"] != "[deleted]":
                    result.append(comment[i]["data"]["body"])
        return result

    def get_date(self,date):
        converted_date = datetime.fromtimestamp(date)
        res = converted_date
        return res

