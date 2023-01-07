from crypt import methods
import imp
import logging
import json 
import os
from urllib import response
from flask import request, jsonify,Blueprint
from subredditClass.subreddit_functions import SubredditF
subreddit_routes = Blueprint('subreddit',__name__)

@subreddit_routes.route("/subreddit_posts", methods = ['GET'])
def subreddit_get_posts():
  sub = SubredditF()
  res = sub.get_hot_posts('Canada',20)
  response = jsonify(
    authError=True,
    data={
      'data': res
    }
  )
  return response

@subreddit_routes.route("/subreddit_comments", methods = ['GET'])
def subreddit_get_comments():
  sub = SubredditF()
  res = sub.get_hot_comments('Canada',20)
  response = jsonify(
    authError=True,
    data={
      'data': res
    }
  )
  return response