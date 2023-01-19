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
import itertools


class TrendsF:
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

    async def get_trend_posts(self, subredditName, query):
        result = []
        subreddit = await self.reddit.subreddit(subredditName)
        async for submission in subreddit.search(query, sort="hot", time_filter="year"):
            date = self.get_date(submission.created_utc)
            res_object = {
                "author": str(submission.author),
                "date": str(date.day) + "/" + str(date.month) + "/" + str(date.year),
                "id": submission.id,
                "name": submission.name,
                "over_18": submission.over_18,
                "num_commenta": submission.num_comments,
                "upvote_ratio": submission.upvote_ratio,
                "subreddit": subredditName,
            }
            result.append(res_object)

        return result

    async def get_result(self, subreddits, keywords):
        arguments = []
        for i in subreddits:
            for j in keywords:
                arguments.append((i, j))

        result = await asyncio.gather(
            *[self.get_trend_posts(x, y) for x, y in arguments]
        )
        await self.reddit.close()
        await self.session.close()
        return list(itertools.chain(*result))

    def get_date(self, date):
        converted_date = datetime.fromtimestamp(date)
        res = converted_date
        return res
