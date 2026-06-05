from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

data = pd.read_csv("siteA.csv")

@app.route("/")
def home():
    return "Site A Running"

@app.route("/students")
def students():
    return jsonify(data.to_dict(orient="records"))

@app.route("/count")
def count():
    return {"site": "A", "records": len(data)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)