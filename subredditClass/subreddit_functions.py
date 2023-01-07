from flask import redirect
import praw
from os import environ
from praw.models import MoreComments



class SubredditF:
  
  def __init__(self) -> None:

    self.reddit = praw.Reddit(
    client_id=environ.get('CLIENT_ID'),
    client_secret=environ.get('SECRET_ID'),
    user_agent="Trenddit/0.0.2",
    refresh_token='2350269160941-tBMkp2mTTMS_UUidLWbSwazOXzP4CA',
    username=environ.get('USER_ID'),
    password=environ.get('PASSWORD'),
    )

    self.reddit.read_only = True



  def get_hot_posts(self,subredditName,num):
    res = []
    subreddit = self.reddit.subreddit(subredditName)
    for submission in subreddit.hot(limit=num):
      print(submission.id)
      res.append(submission.title)
    return res
  
  def get_hot_comments(self,subredditName,num):
    res = []
    uuids = []
    subreddit = self.reddit.subreddit(subredditName)
    for submission in subreddit.hot(limit=num):
      uuids.append(submission.id)
    
    for i in uuids:
      submission = self.reddit.submission(i)
      submission.comments.replace_more(limit=0)
      for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
          continue
        print(top_level_comment.body)
        res.append((top_level_comment.body))
    return res
