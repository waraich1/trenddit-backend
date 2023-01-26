from ast import Return
from itertools import tee
from flask import redirect
import asyncpraw
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


class SubredditF:
    def __init__(self, token) -> None:

        self.reddit = asyncpraw.Reddit(
            client_id=environ.get("CLIENT_ID"),
            client_secret=environ.get("SECRET_ID"),
            user_agent="Trenddit/0.0.2",
            refresh_token=token,
            username=environ.get("USER_ID"),
            password=environ.get("PASSWORD"),
        )
        self.token = token
        self.reddit.read_only = True
        self.session = ClientSession()

    def __aiter__(self):
        return self.__wrapped__.__aiter__()

    async def get_hot_posts(self, subredditName, num):
        res = []
        result = dict()
        text = ""
        subreddit = await self.reddit.subreddit(subredditName)
        async for submission in subreddit.hot(limit=num):
            # date = self.get_date(submission.created_utc)
            date = self.get_date(submission.created_utc)
            res.append(
                {
                    "title": submission.title,
                    "date": str(date.day)
                    + "/"
                    + str(date.month)
                    + "/"
                    + str(date.year),
                    "author": str(submission.author),
                    "nsfw": submission.over_18,
                    "upvote_ratio": submission.upvote_ratio,
                    "score": submission.score
                }
            )
            without_escape = re.sub("[^A-Za-z0-9]+", " ", submission.title)
            text = text + " " + without_escape
        author_score = dict()
        date_counter = Counter(item["date"] for item in res)
        result['date_freq'] = dict(date_counter)
        author_counter = Counter(item["author"] for item in res).most_common(15)
        for item in res:
            author_score[item["author"]] = (
                author_score.get(item["author"], 0) + (item['score'])
            )
        author_score = Counter(author_score).most_common(15)
        result['auth_freq'] = dict(author_counter)
        nsfw_counter = Counter(item["nsfw"] for item in res)
        result['nsfw_freq'] = dict(nsfw_counter)
        upvote_counter = Counter(item["upvote_ratio"] for item in res)
        result['upvote_freq'] = dict(upvote_counter)
        result['trend_freq'] = self.get_freq(text)
        result['author_score'] = dict(author_score)
        await self.session.close()
        await self.reddit.close()
        return result

    async def get_hot_comments(self, subredditName, num):
        res = []
        uuids = []
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        }

        res = []
        uuids = []
        subreddit = await self.reddit.subreddit(subredditName)
        async for submission in subreddit.hot(limit=num):
            url = self.make_url(submission.id, "hot", False)
            res.append(url)

        res = await self.do_tasks(res, headers)
        result = self.convert_hot_comment_result(res)
        await self.reddit.close()
        text_result = self.get_freq(result["text"])
        author_comm_freq = dict(Counter(result["author_comm_freq"]).most_common(15))
        author_score = dict(Counter(result["author_score"]).most_common(15))

        return {"text": text_result, "author_by_comments": author_comm_freq, "author_by_score": author_score}

    def make_url(self, id, sort, threaded):
        return f"http://oauth.reddit.com/comments/{id}?sort={sort}&threaded={threaded}"

    def convert_hot_comment_result(self, res):
        text = " "
        authors_by_comments = dict()
        authors_by_score = dict()
        # print(res[0].json())
        for i in res:
            data = i.json()
            res = data[1]["data"]["children"]
            comment = data[1]["data"]["children"]
            for i in range(len(comment)):
                if (
                    "body" in comment[i]["data"]
                    and comment[i]["data"]["body"] != "[deleted]"
                ):
                    without_url = re.sub(
                        r"\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*",
                        "",
                        comment[i]["data"]["body"],
                        flags=re.MULTILINE,
                    )
                    without_escape = re.sub("[^A-Za-z0-9]+", " ", without_url)
                    author_name = comment[i]["data"]["author"]
                    authors_by_comments[author_name] = (
                        authors_by_comments.get(author_name, 0) + 1
                    )
                    authors_by_score[author_name] = (
                        authors_by_score.get(author_name, 0) + (comment[i]['data']['score'])
                    )
                    text = text + " " + without_escape
        return {"text": text, "author_comm_freq": authors_by_comments, "author_score": authors_by_score}

    def get_date(self, date):
        converted_date = datetime.fromtimestamp(date)
        res = converted_date
        return res

    def get_freq(self, text):
        nlp = en_core_web_sm.load()
        # nlp.max_length = len(text)
        docx = nlp(text)
        nouns = [
            token.text
            for token in docx
            if token.is_stop != True and token.is_punct != True and token.pos_ == "NOUN"
        ]
        freq = Counter(nouns).most_common(200)
        res = dict(freq)
        return res

    async def do_tasks(self, res, headers):
        async with httpx.AsyncClient() as client:
            tasks = [
                client.get(url, headers=headers, follow_redirects=True) for url in res
            ]
            result = await asyncio.gather(*tasks)
            await self.reddit.close()
            await self.session.close()
            return result
