from re import sub
import asyncpraw
from os import environ
import asyncio
from aiohttp import ClientSession
import praw
import requests


auth = requests.auth.HTTPBasicAuth(environ.get("CLIENT_ID"), environ.get("SECRET_ID"))
# here we pass our login method (password), username, and password
data = {
    "grant_type": "password",
    "username": environ.get("USER_ID"),
    "password": environ.get("PASSWORD"),
}
# setup our header info, which gives reddit a brief description of our app
headers = {"User-Agent": "Trenddit/0.0.2"}


def get_author_details():
    reddit = praw.Reddit(
        client_id=environ.get("CLIENT_ID"),
        client_secret=environ.get("SECRET_ID"),
        user_agent="Trenddit/0.0.2",
        refresh_token="2350269160941-qXus-QHk_R1RP3eIRF9mkOCHW3K6zQ",
        username=environ.get("USER_ID"),
        password=environ.get("PASSWORD"),
    )
    username = "nishannntt"
    user = reddit.redditor(username)
    comment_karma = user.comment_karma
    post_karma = user.link_karma
    least_popular_post = {"score": float("inf")}
    most_popular_post = {"score": float("-inf")}
    least_popular_comment = {"score": float("inf")}
    most_popular_comment = {"score": float("-inf")}
    total_karma_req = requests.get(
        f"https://www.reddit.com/user/{username}/about.json",
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

    for link in submissions:
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

    for comment in comments:
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
    average_karma_post = post_karma / total_posts
    average_karma_comment = comment_karma / total_comments

    return {
        "posts": post_details,
        "comments": comment_details,
        "total_posts": total_posts,
        "total_comments": total_comments,
        "comment_karma": comment_karma,
        "post_karma": post_karma,
        "least_popular_post": least_popular_post,
        "most_popular_post": most_popular_post,
        "least_popular_comment": least_popular_comment,
        "most_popular_comment": least_popular_comment,
        "average_karma_post": average_karma_post,
        "average_karma_comment": average_karma_comment,
        "total_karma": total_karma,
    }

    # self_comments = []
    # for comment in comments:
    #     self_comments.append(comment)
    # print(len(self_comments))
    # print(user_details)


# print self_texts
#     print(redditor.link_karma)
#     # karma = redditor.karma()
#     return redditor
# async for submission in redditor.hot(limit=20):
#     res.append(
#         {
#             "title": submission.title,
#             "author": str(submission.author),
#             "nsfw": submission.over_18,
#             "upvote_ratio": submission.upvote_ratio,
#         }
#     )
# return res


res = get_author_details()
print(res)

# res = asyncio.run(get_author_details())
# print(res)
