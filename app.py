from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db


@app.route("/")
def index():
    outputs = db.mars_data.find()
    return render_template("index.html", outputs=outputs)


@app.route("/scrape")
def scrape():
    outputs = db.mars_data
    output_data = scrape_mars.scrape()
    return redirect("http://127.0.0.1:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=False)