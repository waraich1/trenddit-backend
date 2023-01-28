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
    token = FirebaseC().get_token()
    sub = TrendsF(token)
    print(request.base_url)
    res = await sub.get_result(
        ["canada", "ukraine", "australia"],
        ["War", "Russia", "Inflation", "Immigration"],
    )
    response = jsonify(authError=False, data={"data": res})
    return response
