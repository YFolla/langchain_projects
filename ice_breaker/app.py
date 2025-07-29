from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from ice_breaker import ice_break_with

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.form
    name = data.get("name")
    summary, photo_url = ice_break_with(name=name)
    return jsonify({
        "summary_and_facts": summary.to_dict(),
        "picture_url": photo_url or "https://via.placeholder.com/300x300?text=No+Image",
        "ice_breakers": {"ice_breakers": ["Coming soon..."]},
        "interests": {"topics_of_interest": ["Coming soon..."]}
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
    