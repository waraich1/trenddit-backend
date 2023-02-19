from urllib import response

from numpy import equal
from application import app
import json
from unittest import TestCase
import pytest
import requests


def test_subreddit_posts_new():
    params = {"subreddit": "australia", "sort": "New", "top": ""}
    response = app.test_client().get("/subreddit_comments", query_string=params)
    result = response.get_data()
    print(result)


test_subreddit_posts_new()
