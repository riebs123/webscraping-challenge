from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)



@app.route("/")
def welcome():
    data = mongo.db.items.find_one()

    return render_template("index.html", mars=data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # Run the scrape function
    mars = mongo.db.items
    mars_data = scrape_mars.scrape()
    mars.replace_one({}, mars_data, upsert=True)
    
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
