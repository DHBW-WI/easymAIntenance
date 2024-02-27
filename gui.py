from flask import Flask, render_template, request
from gpt_API import call_gpt

gui = Flask(__name__)

@gui.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        call_gpt(request.form.get("inputField"))
    return render_template("index.html")

gui.run(host="0.0.0.0", port=5000)
