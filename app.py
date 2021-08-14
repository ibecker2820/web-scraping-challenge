from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/marssite")

@app.route("/")
def index():
    marssite = mongo.db.collection.find_one()
    return render_template("index.html", marssite=marssite)

@app.route("/scrape")
def scrape():

    marspagedata = scrape_mars.scrape()
    mongo.db.collection.update({}, marspagedata, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)