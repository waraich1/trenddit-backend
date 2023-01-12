from crypt import methods
import imp
import logging
import json
import os
from urllib import response
from flask import request, jsonify, Blueprint
from trendsClass.trends_function import TrendsF

trends_routes = Blueprint("trends", __name__)


@trends_routes.route("/trend_posts", methods=["GET"])
def subreddit_get_posts():
    sub = TrendsF()
    res = sub.get_trend_posts("Canada", "Justin")
    response = jsonify(authError=True, data={"data": res})
    return response
