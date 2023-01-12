import requests
from os import environ
import json


def get_comment(postId, sort, threaded):
    payload = {}
    url = f"http://oauth.reddit.com/comments/{postId}?sort={sort}&threaded={threaded}"
    headers = {
        "Authorization": "Bearer 2350269160941-FKA0VLqcDpasC0vhUl-tX5-HZScZ6w",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    }
    res = requests.get(url, headers=headers, data=payload)
    data = res.json()
    result = []
    res = data[1]["data"]["children"]
    comment = data[1]["data"]["children"]
    for i in range(len(comment)):
        if "body" in comment[i]["data"] and comment[i]["data"]["body"] != "[deleted]":
            result.append(comment[i]["data"]["body"])

    return result
