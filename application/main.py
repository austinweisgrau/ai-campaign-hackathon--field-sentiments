import logging
import os
import secrets
import datetime
import uuid

from flask import Flask, jsonify, render_template, request

from utilities.orm.methods import load_rows_to_database, query, fetch_report
from utilities.orm.models import BatchAnalysis, CanvassResult
from utilities.llm.methods import assemble_prompt, query_gpt

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


@app.route("/api/receive_memo", methods=["POST"])
def receive_memo():
    response = request.get_json()
    data = jsonify(response)
    canvass_result = CanvassResult(
        geo_lat=data["geo_lat"],
        geo_long=data["geo_long"],
        memo=data["memo"],
        created_at=datetime.datetime.now(),
        canvass_result_id=str(uuid.uuid4()),
    )
    load_rows_to_database(canvass_result)
    return 200


@app.route("/generate_report")
def generate_report():
    query_response = query("select memo from canvassresult")
    all_memos: list[str] = [row[0] for row in query_response]
    gpt_prompt = assemble_prompt(all_memos)
    gpt_output = query_gpt(gpt_prompt)
    batch_analysis = BatchAnalysis(
        batch_analysis_id=str(uuid.uuid4()),
        gpt_input_prompt=gpt_prompt,
        gpt_output=gpt_output,
        created_at=datetime.datetime.now(),
    )
    load_rows_to_database(batch_analysis)


@app.route("/report")
def report():
    generate_report()
    result = fetch_report()
    return result
