from crypt import methods
import imp
import logging
import json
import os
from urllib import response
from flask import request, jsonify, Blueprint
from trendsClass.trends_function import TrendsF
from firebase_tools.firebase_tools import FirebaseC
import time
import asyncio

trends_routes = Blueprint("trends", __name__)


@trends_routes.route("/trend_posts", methods=["GET"])
async def subreddit_get_posts():
    trends = request.args.get('trend').split(",")
    subreddits = request.args.get('subreddit').split(",")
    print(trends)
    print(subreddits)
    token = FirebaseC().get_token()
    sub = TrendsF(token)
    res = await sub.get_result(
        subreddits,
        trends,
    )
    response = jsonify(authError=False, data={"data": res})
    return response
