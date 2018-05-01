# import dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
from selenium import webdriver
import time


def scrape():
    import pymongo
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    mars_data = db.mars_data
    db.mars_data.drop()

    outputs = {}
    driver = webdriver.Chrome()

    url = 'https://mars.nasa.gov/news/'
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    title = soup.find('div', class_='bottom_gradient').text

    paragraph = soup.find('div', class_='rollover_description_inner').text

    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    executable_path = {'executable_path': './chromedriver'}
    browser = Browser('chrome', **executable_path)
    browser.visit(img_url)

    browser.click_link_by_id('full_image')
    time.sleep(5)

    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    featured_image_url = browser.find_by_tag('img')[6]['src']

    # twitter url
    twitter_url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response_twitter = requests.get(twitter_url) 

    # create BeautifulSoup object
    soup = BeautifulSoup(response_twitter.text, 'html.parser')

    results_twitter = soup.find('div', class_='js-tweet-text-container')

    mars_weather = results_twitter.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    facts_url = 'https://space-facts.com/mars/'

    # scrape the table data from the page
    tables = pd.read_html(facts_url)

    # create a dataframe
    facts_df = tables[0]
    facts_df.columns = ['Description', 'Value']

    # reset the index
    facts_df.set_index('Description', inplace=True)

    html_table = facts_df.to_html()
    # remove the newline code
    html_table.replace('\n', '')

    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    executable_path = {'executable_path': './chromedriver'}
    browser = Browser('chrome', **executable_path)

    browser.visit(astro_url)

    hemispheres = browser.find_by_css('h3')
    for h in hemispheres:
        print(h.text)

    hem1 = browser.find_by_css('h3')[0].text
    sphere1 = hem1.replace('Enhanced', '')
    hem2 = browser.find_by_css('h3')[1].text
    sphere2 = hem2.replace('Enhanced', '')
    hem3 = browser.find_by_css('h3')[2].text
    sphere3 = hem3.replace('Enhanced', '')
    hem4 = browser.find_by_css('h3')[3].text
    sphere4 = hem4.replace('Enhanced', '')

    browser.find_by_css('h3')[0].click()
    hem1_img = browser.find_by_tag('a')[41]['href']
    browser.back()

    browser.find_by_css('h3')[1].click()
    hem2_img = browser.find_by_tag('a')[41]['href']
    browser.back()

    browser.find_by_css('h3')[2].click()
    hem3_img = browser.find_by_tag('a')[41]['href']
    browser.back()

    browser.find_by_css('h3')[3].click()
    hem4_img = browser.find_by_tag('a')[41]['href']
    browser.back()

    # save the title and url using a Python dictionary
    hemisphere_dict = [
        {"name": sphere1, "url": hem1_img},
        {"name": sphere2, "url": hem2_img},
        {"name": sphere3, "url": hem3_img},
        {"name": sphere4, "url": hem4_img}
        ]


    outputs = {'title': title,
        'paragraph': paragraph,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'html_table': html_table,
        'hemisphere_dict': hemisphere_dict}

    mars_data.insert(outputs)
    return outputs


