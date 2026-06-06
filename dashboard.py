from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def dashboard():

    nodes = [
        ("Site A","http://127.0.0.1:5001/count"),
        ("Site B","http://127.0.0.1:5002/count"),
        ("Site C","http://127.0.0.1:5003/count")
    ]

    result = []
    total = 0

    for name,url in nodes:

        try:

            r = requests.get(url,timeout=2)
            data = r.json()

            records = data["records"]

            total += records

            result.append({
                "name":name,
                "status":"ONLINE",
                "records":records
            })

        except:

            result.append({
                "name":name,
                "status":"OFFLINE",
                "records":0
            })

    return render_template(
        "dashboard.html",
        nodes=result,
        total=total
    )

if __name__=="__main__":
    app.run(port=8000,debug=True)