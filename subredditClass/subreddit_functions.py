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
from os import cpu_count
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

    async def get_hot_posts(self, subredditName, num, sort, top):
        print(num)
        print(sort)
        print(top)
        res = []
        result = dict()
        text_list = []
        subreddit = await self.reddit.subreddit(subredditName)
        submissions = None
        await subreddit.load()
        name = str(subreddit.display_name)
        if sort == "Hot":
            submissions = subreddit.hot(limit=num)
        elif sort == "New":
            submissions = subreddit.new(limit=num)
        else:
            if top == "AllTime":
                submissions = subreddit.top(
                    limit=num,
                )
            elif top == "Week":
                submissions = subreddit.top(limit=num, time_filter="week")
            elif top == "Year":
                submissions = subreddit.top(limit=num, time_filter="year")
            else:
                submissions = subreddit.top(limit=num, time_filter="month")

        async for submission in submissions:
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
                    "hour_created": date.hour,
                    "score": submission.score,
                }
            )
            without_escape = re.sub("[^A-Za-z0-9]+", " ", submission.title)
            text_list.append(without_escape)
        author_score = dict()
        hour_counter = Counter(item["hour_created"] for item in res)
        author_counter = Counter(item["author"] for item in res).most_common(20)
        for item in res:
            author_score[item["author"]] = author_score.get(item["author"], 0) + (
                item["score"]
            )
        author_score = Counter(author_score).most_common(20)
        result["name"] = name
        result["auth_freq"] = dict(author_counter)
        nsfw_counter = Counter(item["nsfw"] for item in res)
        result["nsfw_freq"] = dict(nsfw_counter)
        upvote_counter = Counter(item["upvote_ratio"] for item in res)
        result["upvote_freq"] = dict(upvote_counter)
        result["trend_freq"] = await self.get_freq(text_list)
        result["author_score"] = dict(author_score)
        result["hour_counter"] = dict(hour_counter)
        await self.session.close()
        await self.reddit.close()
        return result

    async def get_hot_comments(self, subredditName, num, sort, top):
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
        await subreddit.load()
        name = str(subreddit.display_name)
        submissions = None
        if sort == "Hot":
            submissions = subreddit.hot(limit=num)
        elif sort == "New":
            submissions = subreddit.new(limit=num)
        else:
            if top == "AllTime":
                submissions = subreddit.top(
                    limit=num,
                )
            elif top == "Week":
                submissions = subreddit.top(limit=num, time_filter="week")
            elif top == "Year":
                submissions = subreddit.top(limit=num, time_filter="year")
            else:
                submissions = subreddit.top(limit=num, time_filter="month")
        async for submission in submissions:
            url = self.make_url(submission.id, "hot", False)
            res.append(url)

        res = await self.do_tasks(res, headers)
        result = await self.convert_hot_comment_result(res)
        await self.reddit.close()
        text_result = result["text"]
        author_freq = dict(Counter(result["author_comm_freq"]).most_common(20))
        author_score = dict(Counter(result["author_score"]).most_common(20))

        return {
            "name": name,
            "text": text_result,
            "author": author_freq,
            "hour_freq": result["hour_freq"],
            "author_by_score": author_score,
        }

    def make_url(self, id, sort, threaded):
        return f"http://oauth.reddit.com/comments/{id}?sort={sort}&threaded={threaded}"

    async def convert_hot_comment_result(self, res):
        text = []
        authors = dict()
        hour_freq = dict()
        authors_by_score = dict()
        for i in res:
            data = i.json()
            res = data[1]["data"]["children"]
            comment = data[1]["data"]["children"]
            for i in range(len(comment)):
                if "created_utc" in comment[i]["data"]:
                    hour_created = self.get_date(comment[i]["data"]["created_utc"]).hour
                    hour_freq[hour_created] = hour_freq.get(hour_created, 0) + 1
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
                    author_name = comment[i]["data"]["author"]
                    authors_by_score[author_name] = authors_by_score.get(
                        author_name, 0
                    ) + (comment[i]["data"]["score"])
                    text.append(without_escape)
        res = await self.get_freq(text)
        return {
            "text": res,
            "author_comm_freq": authors,
            "hour_freq": hour_freq,
            "author_score": authors_by_score,
        }

    def get_date(self, date):
        converted_date = datetime.fromtimestamp(date)
        res = converted_date
        return res

    async def get_freq(self, text):

        nlp = en_core_web_sm.load()
        docx = list(nlp.pipe(text, n_process=cpu_count() - 1))
        result = await asyncio.gather(*[self.getNouns(doc) for doc in docx])
        final_result = list(itertools.chain(*result))
        freq = Counter(final_result).most_common(200)
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
