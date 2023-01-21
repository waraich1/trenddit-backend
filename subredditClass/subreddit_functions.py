from ast import Return
from itertools import tee
from flask import redirect
import asyncpraw
from os import environ
from os import cpu_count
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
import time
import itertools


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
        result = []
        text = ""
        text_list = []
        subreddit = await self.reddit.subreddit(subredditName)
        async for submission in subreddit.hot(limit=num):
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
                }
            )
            without_escape = re.sub("[^A-Za-z0-9]+", " ", submission.title)
            text_list.append(without_escape)
        date_counter = Counter(item["date"] for item in res)
        result.append({"date-freq": dict(date_counter)})
        authour_counter = Counter(item["author"] for item in res).most_common(15)
        result.append({"auth-freq": dict(authour_counter)})
        nsfw_counter = Counter(item["nsfw"] for item in res)
        result.append({"nsfw-freq": dict(nsfw_counter)})
        upvote_counter = Counter(item["upvote_ratio"] for item in res)
        result.append({"upvote-freq": dict(upvote_counter)})
        result.append({"trend-freq": self.get_freq(text_list)})
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
        result = await self.convert_hot_comment_result(res)
        await self.reddit.close()
        text_result = result["text"]
        author_freq = dict(Counter(result["author-freq"]).most_common(15))

        return {"text": text_result, "author": author_freq}

    def make_url(self, id, sort, threaded):
        return f"http://oauth.reddit.com/comments/{id}?sort={sort}&threaded={threaded}"

    async def convert_hot_comment_result(self, res):
        text = []
        authors = dict()
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
                    authors[comment[i]["data"]["author"]] = (
                        authors.get(comment[i]["data"]["author"], 0) + 1
                    )
                    text.append(without_escape)
        res = await self.get_freq(text)
        return {"text": res, "author-freq": authors}

    def get_date(self, date):
        converted_date = datetime.fromtimestamp(date)
        res = converted_date
        return res

    async def get_freq(self, text):

        nlp = en_core_web_sm.load()
        docx = list(nlp.pipe(text, n_process=cpu_count() - 1))
        result = await asyncio.gather(*[self.getNouns(doc) for doc in docx])
        final_result = list(itertools.chain(*result))
        freq = Counter(final_result).most_common(20)
        res = dict(freq)

        return res

    async def getNouns(slef, doc):
        nouns = []
        for token in doc:
            if (
                token.is_stop != True
                and token.is_punct != True
                and token.pos_ == "NOUN"
            ):
                nouns.append(token.text)
        return nouns

    async def do_tasks(self, res, headers):
        async with httpx.AsyncClient() as client:
            tasks = [
                client.get(url, headers=headers, follow_redirects=True) for url in res
            ]
            result = await asyncio.gather(*tasks)
            await self.reddit.close()
            await self.session.close()
            return result
