# from crypt import methods
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
    try:
        trends = request.args.get("trend", default="").split(",")
        subreddits = request.args.get("subreddit", default="").split(",")
        if len(trends) == 1 and trends[0] == "":
            response = jsonify(
                data={
                    "success": False,
                    "errorCode": "trend is not provided in request argument",
                }
            )
            response.status_code = 400
            return response
        if len(subreddits) == 1 and subreddits[0] == "":
            response = jsonify(
                data={
                    "success": False,
                    "errorCode": "subreddits is not provided in request argument",
                }
            )
            response.status_code = 400
            return response
        print(trends)
        print(subreddits)
        token = FirebaseC().get_token()
        sub = TrendsF(token)
        print(request.base_url)
        res = await sub.get_result(
            subreddits,
            trends,
        )
        if len(res) == 0:
            response = jsonify(
                data={
                    "success": False,
                    "errorCode": "Trend does not exist",
                }
            )
            response.status_code = 500
            return response
        response = jsonify(authError=False, data={"data": res})

    except Exception as e:
        response = jsonify(data={"success": False, "errorCode": str(e)})
        response.status_code = 500
    return response
