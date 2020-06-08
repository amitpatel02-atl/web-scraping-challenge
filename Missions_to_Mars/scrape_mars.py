#################################################
# Jupyter Notebook Conversion to Python Script
#################################################

#!/usr/bin/env python
# coding: utf-8

# Dependencies and Setup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# Web Site Scraper
def scrape_all():

    #################################################
    # Windows
    #################################################
    # Set Executable Path & Initialize Chrome Browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # Visit the NASA Mars News Site
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    # Create dictionary to store items
    mars={}

    # Parse Results HTML with BeautifulSoup
    # Find Everything Inside:
    # Find the first title and the paragraph of the first title
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    quotes = soup.find_all('div', class_='content_title')
    body = soup.find('div', class_='article_teaser_body')
    print(quotes[1])
    print(body)                        
                            

    # Store the title and paragraph as new_title and news_p
    new_title = quotes[1]
    news_p = body


    # Add new_title and news_p to mars dictionary
    mars["new_title"]=new_title
    mars["news_p"]=news_p


    # Close the brower
    browser.quit()

    # Set Executable Path & Initialize Chrome Browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the JPL Mars News Site
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    # Browse and click on "full image"
    browser.find_by_id("full_image").click()

    # Browse and click on "more info"
    browser.find_link_by_partial_text("more info").click()

    # Parse Results HTML with BeautifulSoup
    # Find Everything Inside:
    # Find the image
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    quotes = soup.find('figure', class_='lede')

    print(quotes)

    # Print htag
    print(quotes.a)

    # Print image
    print(quotes.a.img)

    # Print image jpg
    print(quotes.a.img["src"])

    # Retrieve background-image url from style tag
    featured_image="https://www.jpl.nasa.gov"+quotes.a.img["src"]

    # Dictionary entry from FEATURED IMAGE
    mars["featured_image"]= featured_image

    # Close the brower
    browser.quit()

    # Set Executable Path & Initialize Chrome Browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit Mars Weather Twitter through splinter module
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Add sleep time
    time.sleep(2)

    # HTML Object
    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Compile twitter text by using regular expression
    twitter_text= re.compile(r'sol')
    weather=soup.find('span', text=twitter_text).text
    print(weather)

    #Dictionary entry from twitter
    mars["weather"]=weather

    # Close the brower
    browser.quit()

    # Set Executable Path & Initialize Chrome Browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # HTML Object
    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Visit space facts through splinter module
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # Use Panda's `read_html` to parse the url
    facts_of_planet = pd.read_html(url)
    facts_of_planet

    # Find the facts abbreviations DataFrame in the list of DataFrames as assign it to `df`
    # Assign the columns `['Profile', 'Value']`
    df = facts_of_planet[0]
    df.columns = ['Profile', 'Values']
    df.head()

    # Export dataframe to HTML
    file_html= df.to_html(index=False)

    #Show tablefile_html
    file_html

    # Clean up data and replace '\n' with ''
    file_html.replace('\n', '')

    # Export file to HTML
    with open('outputfile.html', 'w') as df:
        df.write(file_html)

    # Close the brower
    browser.quit()

    # Set Executable Path & Initialize Chrome Browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the Mars hemisphere Site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Store images in a dictionary
    hemisphere_image_urls = []

    # Find Element on Each Loop to Avoid a Stale Element Exception
    hemispheres_links= browser.find_by_css("a.product-item h3")
    hemispheres_links

    # Loop through the items previously stored
    for i in range(len(hemispheres_links)):
        hemispheres={}

        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[i].click()

        # Find Sample Image Anchor Tag & Extract <href>
        sample_element=browser.find_link_by_text('Sample').first
        hemispheres["img_url"]=sample_element['href']

        # Get Hemisphere Title
        hemispheres["title"]=browser.find_by_css("h2.title").text

        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemispheres)

        # Navigate Backwards
        browser.back()

    hemisphere_image_urls

    # Dictionary entry from hemispheres website
    mars["hemispheres"]=hemisphere_image_urls

    return mars
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())