# coding: utf-8

# # Misson to Mars

# # Step 1 - Scraping
# -------
# ## NASA Mars News
# -------
# - Get the latest  [NASA Mars News](https://mars.nasa.gov/news/) by scraping the website and collect the latest news title and paragragh text.

# Import dependencies
import bs4
from bs4 import BeautifulSoup
import requests
import splinter
from splinter import Browser
import pandas as pd


def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # save the most recent article, title and date
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text
    print(news_date)
    print(news_title)
    print(news_p)

    # Visit the JPL Mars URL
    url2 = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    # Scrape the browser into soup and use soup to find the image of mars
    # Save the image url to a variable called `img_url`
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find("img", class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url
    # Use the requests library to download and save the image from the `img_url` above
    import requests
    import shutil
    response = requests.get(img_url, stream=True)
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
        
    # Display the image with IPython.display
    from IPython.display import Image
    Image(url='img.jpg')

    # #### Mars Weather using twitter

    #get mars weather's latest tweet from the website
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html
    soup = BeautifulSoup(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather

    url = 'https://space-facts.com/mars/'

    ### creating tables from webpage

    tables = pd.read_html(url)
    tables

    ### creating the table

    df = tables[0]
    df.columns = ['Item','Value']
    df

    df=df.set_index("Item")
    df

    marsdata = df.to_html(classes='marsdata')
    marsdata = marsdata.replace('\n', ' ')
    marsdata

    # Visit the USGS Astogeology site and scrape pictures of the hemispheres
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)

    # Use splinter to loop through the 4 images and load them into a dictionary
    import time 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_hemis=[]

    # loop through the four tags and load the data to the dictionary

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()

    output = {'news_title':news_title, 'news_p':news_p, 'img_url':img_url,
              'mars_weather':mars_weather,'marsdata':marsdata, 'images':images}
   
    return output
