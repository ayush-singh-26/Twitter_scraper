from flask import Flask, render_template, jsonify
import subprocess
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['mongodb_url'] = os.getenv('MONGODB_URI')

client = MongoClient(app.config['mongodb_url'])
db = client["twitter_trends"]
collection = db["trends"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-script")
def run_script():
    subprocess.run(["python", "twitter_scraper.py"])
    return "Script executed successfully!"

@app.route("/results")
def results():
    latest_record = collection.find_one(sort=[("timestamp", -1)])
    return jsonify(latest_record)

if __name__ == "__main__":
    app.run(debug=True)
