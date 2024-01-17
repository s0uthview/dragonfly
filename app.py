"""Main application logic for Dragonfly."""
import pytz
import os

from dotenv import load_dotenv
from datetime import datetime
from secrets import token_urlsafe

from flask import Flask, render_template, request, redirect, abort, flash
from flask_bootstrap import Bootstrap

from faunadb import query as q
from faunadb.client import FaunaClient

from util.jinjamd import MarkdownExtension

# load the .env file
load_dotenv()

# create application and initialize bootstrap
app = Flask(__name__, static_folder="static")
app.jinja_env.add_extension(MarkdownExtension)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# load bootstrap for flask app
Bootstrap(app)

# create database connection
client = FaunaClient(secret=os.getenv("FAUNA_DB_SECRET"))


def _check_paste_id(paste_id):
    # helper function to check if an paste_id already exists
    exists = client.query(q.exists(
            q.match(q.index("paste_by_paste_id"), paste_id)))

    if exists:
        return True
    return False


@app.route("/", methods=["GET", "POST"])
def index():
    """The logic behind creating new pastes.

    Methods:
        GET: Retrieves the form for creating and uploading a new paste.
        POST: Uploads a new paste to Dragonfly, and redirects the user to their new paste.
    """
    if request.method == "POST":
        paste_title = request.form.get("title").strip()
        paste_text = request.form.get("paste-text").strip()
        paste_destructing = request.form.get("paste-destructing") or False
        paste_id = request.form.get("paste_id")

        if _check_paste_id(paste_id):
            flash("A paste already exists with this paste_id.", "danger")
            return redirect(request.host_url)

        if paste_id == '':
            paste_id = token_urlsafe(7)

        client.query(q.create(q.collection("pastes"), {
            "data": {
                "paste_id": paste_id,
                "paste_text": paste_text,
                "paste_title": paste_title,
                "paste_destructing": paste_destructing,
                "paste_date": datetime.now(pytz.UTC)  # use pytz to provide accurate dating info
            }
        }))

        if paste_destructing == "on":
            flash(f"Self destructing paste created! Your paste can be found here: {request.host_url + paste_id}", "info")
            return redirect(request.host_url)
        return redirect(request.host_url + paste_id)
    return render_template("index.html")


@app.route("/<string:paste_id>/")
def render_paste(paste_id):
    """The logic for retrieving a post's contents from the database and displaying them.

    Args:
        paste_id: The paste_id for the paste.

    Methods:
        GET: Retrieves a post from the database.
    """
    try:
        paste = client.query(
            q.get(q.match(q.index("paste_by_paste_id"), paste_id)))

        if paste["data"]["paste_destructing"] == "on":
            # alert the user that this message is self-destructing
            flash("This paste is self-destructing and can only be viewed once.", "info")
            # destroy the paste
            client.query(
                q.delete(paste["ref"]))  # this is a janky ass method to delete something from fauna lmao
    except:
        abort(404)

    return render_template("paste.html", paste=paste["data"])


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")
