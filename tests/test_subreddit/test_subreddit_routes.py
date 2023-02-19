from urllib import response

from numpy import equal
from application import app
import json
from unittest import TestCase
import pytest
import requests


def test_basic_route():
    response = app.test_client().get("/")
    result = response.get_data()
    test_result = json.loads(result.decode("utf-8"))
    TestCase().assertDictEqual(test_result, {"message": "Trenddit Backend!"})


def test_subreddit_posts_hot():
    params = {"subreddit": "canada", "sort": "Hot", "top": ""}
    response = app.test_client().get("/subreddit_comments", query_string=params)
    result = response.get_data()
    result_string = result.decode("utf-8")
    result_json = json.loads(result_string)
    assert len(result_json["data"]["author"]) > 2
    assert len(result_json["data"]["author_by_score"]) > 2
    assert result_json["data"]["name"] == "canada"
    assert len(result_json["data"]["text"]) > 5
    assert response.status_code == 200


def test_subreddit_posts_top():
    params = {"subreddit": "india", "sort": "Top", "top": "Month"}
    response = app.test_client().get("/subreddit_comments", query_string=params)
    result = response.get_data()
    result_string = result.decode("utf-8")
    result_json = json.loads(result_string)
    assert len(result_json["data"]["author"]) > 2
    assert len(result_json["data"]["author_by_score"]) > 2
    assert result_json["data"]["name"] == "india"
    assert len(result_json["data"]["text"]) > 5
    assert response.status_code == 200


def test_subreddit_posts_new():
    params = {"subreddit": "australia", "sort": "New", "top": ""}
    response = app.test_client().get("/subreddit_comments", query_string=params)
    result = response.get_data()
    text_file = open("data.txt", "w")

    result_string = result.decode("utf-8")
    text_file.write(str(result))

    # close file
    text_file.close()
    result_json = json.loads(result_string)
    assert len(result_json["data"]["author"]) > 2
    assert len(result_json["data"]["author_by_score"]) > 2
    assert result_json["data"]["name"] == "australia"
    assert len(result_json["data"]["text"]) > 5
    assert response.status_code == 200
