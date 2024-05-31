import logging
import os
import secrets
import uuid
from datetime import datetime

from flask import Flask, jsonify, render_template, request
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from utilities.orm.methods import load_rows_to_database, query
from utilities.orm.models import BatchAnalysis, CanvassResult

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


@app.route("/report")
def report():
    all_memos = query("select memo from canvassresult")
    gpt_prompt = assemble_prompt(all_memos)
    gpt_output = query_gpt(gpt_prompt)
    batch_analysis = BatchAnalysis(
        batch_analysis_id=str(uuid.uuid4()),
        gpt_input_prompt=gpt_prompt,
        gpt_output=gpt_output,
        created_at=datetime.datetime.now(),
    )
    load_rows_to_database(batch_analysis)
    report = assemble_report()
    return report


def assemble_prompt(all_memos: list[str]) -> str:
    """Take all memos and assemble prompt for GPT summarization/analysis."""
    # Format all memos into a list of h2 tags
    all_memos_formatted = "\n".join([f"<h2>{memo}</h2>" for memo in all_memos])

    template = """
    <transcripts>
    {all_memos}
    </ transcripts>

    <instructions>
    ## Analyze the transcripts and summarize them into 3 overall topics of concern or sentiment.
    ## Each topic or concern should be only one or two sentences.
    ## ONLY use the terminology and details used by the doorknockers in <transcripts>. Do not use synonyms or more general categories.
    ## Do not mention voter names.
    ## Write only the topic or concern an no other text.
    <instructions />
    """

    result = template.format(all_memos=all_memos_formatted)

    return result


def query_gpt(gpt_prompt: str) -> str:
    """Hit LLM API with gpt prompt, return response."""
    if not "OPENAI_API_KEY" in os.environ:
        raise KeyError("Set OPENAI_API_KEY in environment.")

    chat = ChatOpenAI(model_name="gpt-4o", temperature=1)
    initial_response = chat(
        [
            SystemMessage(
                content="The following text contained in <transcripts /> is a set of voice transcripts of doorknockers in Mississippi ahead of an election. The doorknockers are talking with potential voters regarding their plans for voting during the election, and trying to answer questions for any concerns the voters may have."
            ),
            HumanMessage(content=gpt_prompt),
        ]
    )

    reframe_response = chat(
        [
            initial_response,
            HumanMessage(
                content="Reframe the above topics into questions or prompts that the doorknockers can weave into future conversations with voters.\n\nThe questions should be causal and understandable to a rural audience."
            ),
        ]
    )

    result = f"{initial_response.content}\n\nScript Recommendations:\n\n{reframe_response.content}"

    return result


def assemble_report() -> str:
    """Assemble report based on latest batch analysis."""
    latest_analysis = query(
        "select gpt_output from batchanalysis order by created_at desc limit 1"
    )
    raise NotImplementedError
