import requests
import feedparser

from flask import Flask, render_template

from random import sample

app = Flask(__name__)


FLICKR_API_KEY = "f43b2dbc2b7f78016bcf4c2814191346"
WEATHER_API_KEY = "79f58546fcd5877957e0df2eb6b17ecb"


@app.route('/')
def index():
    """
    This function displays the main kiosk page.
    """

    # Grab the weather.
    weather = fetch_weather()

    # Grab the news.
    news = fetch_news(5)

    # Grab some photos
    photos = fetch_photos(5)

    return render_template('index.html', photos=photos, news=news, weather=weather)


@app.route('/map/')
def map():
    """
    This function displays the map page.
    """
    return render_template('map.html')


@app.route('/credits/')
def credits():
    """
    This function displays the credits page.
    """
    return render_template('credits.html')


def fetch_weather():
    """
    This function fetches the current weather.
    """

    # Fetch the current weather.
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q=Manchester,UK&units=metric&APPID={WEATHER_API_KEY}')

    # Return the data.
    return response.json()


def fetch_news(n):
    """
    This function fetches news articles.
    """

    # This is the list we will use the pass back the news information.
    data = []

    # Get news stories from the MEN RSS feed.
    response = feedparser.parse('https://www.manchestereveningnews.co.uk/?service=rss')

    # Loop through the news items, and the pull out the data we need.
    for news in response.entries[:n]:
        data.append({
            'headline': news.title,
            'content': news.description,
        })

    return data


def fetch_photos(n):
    """
    This function fetches photos from Flickr.
    """

    # This is the list we will use the pass back the photo information.
    data = []

    # First, we search for photos taken in Manchester.
    response = requests.get(f'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={FLICKR_API_KEY}&tags=Manchester&format=json&nojsoncallback=1')

    # Now loop through the photos.
    for photo in sample(response.json()['photos']['photo'], n):

        # We will search with the photo ID.
        id = photo['id']

        # Get the photo details. We can get the URL to the photo from here.
        response = requests.get(f'https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key={FLICKR_API_KEY}&photo_id={id}&format=json&nojsoncallback=1')

        # Extract the photo URL from the response.
        url = response.json()['sizes']['size'][-1]['source']

        # Store our photo ID and URL.
        data.append({
            'id': photo['id'],
            'url': url
        })

    # Send back our list of photos.
    return data
