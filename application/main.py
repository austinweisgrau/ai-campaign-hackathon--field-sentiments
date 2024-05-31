import logging
import secrets
from datetime import datetime

from flask import Flask, jsonify, render_template, request
from utilities.orm.methods import load_rows_to_database, query
from utilities.orm.models import User

logger = logging.getLogger(__name__)

app = Flask(
    __name__,
    static_folder="../frontend/",
    static_url_path="/",
    template_folder="../frontend/",
)

# Fine to set this once at import time
app.secret_key = secrets.token_urlsafe(16)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test_db_connection")
def test_db_connection():
    response = query("select session_user")
    return f"<div>Database response: {response}</div>"
