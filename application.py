import argparse
from ast import arguments
import logging

from flask_cors import CORS
from flask import Flask, request, session, abort, jsonify, Blueprint

import api.subreddit as subreddit_routes
import api.trends as trends_routes


app = Flask(__name__)

app.register_blueprint(subreddit_routes.subreddit_routes)
app.register_blueprint(trends_routes.trends_routes)


CORS(app)


@app.route("/")
def index():
    return jsonify({"message": "Trenddit Backend!"})


def parse_args():
    parser = argparse.ArgumentParser(
        description="Start the pg choral backend serverlet"
    )
    parser.add_argument(
        "-ho",
        "--host",
        type=str,
        help="The host for choral application",
        default="0.0.0.0",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help="The port for the application server",
        default=5000,
    )

    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()

    app.run(host=arguments.host, port=arguments.port, debug=True)
