import asyncpraw
from os import environ
import asyncio
from aiohttp import ClientSession


async def get_comments():
    reddit = asyncpraw.Reddit(
        client_id=environ.get("CLIENT_ID"),
        client_secret=environ.get("SECRET_ID"),
        user_agent="Trenddit/0.0.2",
        refresh_token="2350269160941-qXus-QHk_R1RP3eIRF9mkOCHW3K6zQ",
        username=environ.get("USER_ID"),
        password=environ.get("PASSWORD"),
    )
    subreddit = await reddit.subreddit("Canada", fetch=True)
    res = []
    async for submission in subreddit.hot(limit=20):
        res.append(
            {
                "title": submission.title,
                "author": str(submission.author),
                "nsfw": submission.over_18,
                "upvote_ratio": submission.upvote_ratio,
            }
        )
    return res


res = asyncio.run(get_comments())
print(res)
