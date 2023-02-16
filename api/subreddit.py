# from crypt import methods
import imp
import logging
import json
import os
from urllib import response
from flask import request, jsonify, Blueprint
from subredditClass.subreddit_functions import SubredditF
from firebase_tools.firebase_tools import FirebaseC
import asyncio

subreddit_routes = Blueprint("subreddit", __name__)


@subreddit_routes.route("/subreddit_posts", methods=["GET"])
async def subreddit_get_posts():
    try:
        subreddit_name = request.args.get("subreddit")
        sort = request.args.get("sort")
        top = request.args.get("top")
        token = FirebaseC().get_token()
        sub = SubredditF(token)
        res = await sub.get_hot_posts(subreddit_name, 100, sort, top)
        response = jsonify(authError=True, data=res)
    except Exception as e:
        response = jsonify(
            data={
                "success": False,
                "errorCode": "Invalid subreddit name: "
                + subreddit_name
                + " or request:- "
                + str(e),
            }
        )
        response.status_code = 400
    return response


@subreddit_routes.route("/subreddit_comments", methods=["GET"])
async def subreddit_get_comments():
    try:
        subreddit_name = request.args.get("subreddit")
        sort = request.args.get("sort")
        top = request.args.get("top")
        token = FirebaseC().get_token()
        sub = SubredditF(token)
        res = await sub.get_hot_comments(subreddit_name, 50, sort, top)
        response = jsonify(authError=True, data=res)
    except Exception as e:
        response = jsonify(
            data={
                "success": False,
                "errorCode": "Invalid subreddit name: "
                + subreddit_name
                + " or request:- "
                + str(e),
            }
        )
        response.status_code = 400
    return response
