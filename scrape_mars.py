import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Mars News
    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    latest = soup.find('li', class_='slide')

    latest_title = latest.find('div', class_='content_title').text
    latest_paragraph = latest.find('div', class_='article_teaser_body').text

    #JPL Mars Image
    featured_image_url = 'https://spaceimages-mars.com'
    browser.visit(featured_image_url)
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')

    image = image_soup.findAll('img')[1]['src']
    featured_image = featured_image_url + "/" + image

    #Mars Facts
    facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(facts_url)

    info_df = tables[1]
    info_df.columns = ['Fact','Value']
    info_html = info_df.to_html()

    #Mars Hemisphers
    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)
    hemi_html = browser.html
    hemi_soup = bs(hemi_html, 'html.parser')

    items = hemi_soup.findAll('div', class_='item')
    urls = []
    titles = []
    for item in items:
        urls.append(hemisphere_url + item.find('a')['href'])
        titles.append(item.find('h3').text)
    
    img_urls = []
    for ind_url in urls:
        browser.visit(ind_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        ind_url = hemisphere_url+soup.find('img',class_='wide-image')['src']
        img_urls.append(ind_url)

    hemisphere_image_urls = []
    for i in range(len(titles)):
        hemisphere_image_urls.append({'title':titles[i],'img_url':img_urls[i]})

    marssite = {}
    marssite["news_title"] = latest_title
    marssite["news_paragraph"] = latest_paragraph
    marssite["featured_image_url"] = featured_image
    marssite["marsfacts_html"] = info_html
    marssite["hemisphere_image_urls"] = hemisphere_image_urls
    
    return marssite