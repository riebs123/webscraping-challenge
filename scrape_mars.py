import requests
import pymongo
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # Define database and collection
    db = client.mars_db
    collection = db.items
    
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit redplanetscience.com for latest news article

    url = "https://redplanetscience.com"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")


    # Get the latest news article
    news = soup.find('div', class_= 'list_text')

    title = news.find('div', class_= 'content_title').text
    desc = news.find('div', class_= 'article_teaser_body').text


    # Visit spaceimages-mars.com for feature image

    url2 = "https://spaceimages-mars.com/"

    browser.visit(url2)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")


    relative_image_path = soup.find_all('img')[1]['src']

    featured_image = url2 + relative_image_path


    # Visit https://galaxyfacts-mars.com for Mars vs earth comparison

    table = pd.read_html('https://galaxyfacts-mars.com/')

    mars_facts = table[0]
    
    mars_facts_html = mars_facts.to_html()

    mars_facts_html = mars_facts_html.replace('\n', '')

    # Visit https://marshemispheres.com/ for hemispheres of Mars

    url3 = 'https://marshemispheres.com/'

    browser.visit(url3)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    relative_image_path = soup.find_all('img', class_='thumb')


    hemisphere_dict = []

    for x in relative_image_path:

        JArray2 = {}
        JArray2["title"]= x['alt']
        JArray2["img_url"]= url3+x['src']
        hemisphere_dict.append(JArray2)

    data = {
        'news_title': title,
        'news_description': desc,
        'featured_image': featured_image,
        'mars_facts': mars_facts_html,
        'hemisphere_dict':hemisphere_dict
    }
    
    browser.quit()
    
    return data

