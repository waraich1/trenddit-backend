from crypt import methods
import imp
import logging
import json 

import os
from urllib import response
from flask import request, jsonify,Blueprint

subreddit_routes = Blueprint('subreddit',__name__)

@subreddit_routes.route("/subreddit_posts", methods = ['GET'])
def subreddit_get():
  response = jsonify(
    authError=True,
    data={
      'data': 'This works'
    }
  )
  return response