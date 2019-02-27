from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    news = mongo.db.news.find()
    featured_image = mongo.db.featured_image.find()
    facts = mongo.db.facts.find()
    weather = mongo.db.weather.find()
    hemispheres = mongo.db.hemispheres.find()
    return render_template("mars.html", news=news, featured_image=featured_image, facts=facts, weather=weather, hemispheres=hemispheres)

@app.route("/scrape")
def scraper():
    news = mongo.db.news
    news_data = scrape_mars.news_scrape()
    news.update({}, news_data, upsert=True)
    featured_image = mongo.db.featured_image
    featured_image_data = scrape_mars.featured_img_scrape()
    featured_image.update({}, featured_image_data, upsert=True)
    weather = mongo.db.weather
    weather_data = scrape_mars.weather_scrape()
    weather.update({}, weather_data, upsert=True)
    facts = mongo.db.facts
    facts_data = scrape_mars.info_scrape()
    # drop all documents before doing this, so you only have recent ones
    facts.delete_many({})
    facts.insert_many(facts_data)
    hemispheres = mongo.db.hemispheres
    hemispheres_data = scrape_mars.hemi_scrape()
    hemispheres.delete_many({})
    hemispheres.insert_many(hemispheres_data)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)