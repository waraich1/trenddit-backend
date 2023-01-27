from crypt import methods
import imp
import logging
import json
import os
from urllib import response
from flask import request, jsonify, Blueprint
from authorClass.author_function import AuthorF
from firebase_tools.firebase_tools import FirebaseC
import time
import asyncio

author_routes = Blueprint("author", __name__)


@author_routes.route("/author_details", methods=["GET"])
async def subreddit_get_posts():
    token = FirebaseC().get_token()
    user = AuthorF(token)
    res = await user.get_author_details()
    response = jsonify(authError=False, data={"data": res})
    return response
