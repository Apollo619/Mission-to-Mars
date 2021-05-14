# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_images(browser),
        "facts": mars_facts(browser),
        "last_modified": dt.datetime.now(),
        "mars_hemi": mars_hemi(browser)
        }
        
    

    # Stop webdriver and return data
    browser.quit()
    return data

# Visit the mars nasa news site
def mars_news(browser):
    
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_ ='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# Visit URL Mars image
def featured_images(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'


    return img_url

    ## Mars Facts
def mars_facts(browser):
    # Add try/except for error handling
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    
    # Assign columns and set index to dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    # convert dataframe into HTML format, add bootstrap
    return df.to_html()

    ## Mars Hemispheres
def mars_hemi(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    link_soup = soup(html, 'html.parser')

    links = link_soup.find_all('div', class_='item')

    # loop through links to select hemispheres
    for i in range(0,4):
        hemispheres = {}
        
        # Go to the website
        browser.visit(url) 
        
        # Find tag to select the link
        img_thumb = browser.find_by_css(".thumb")[i]
        # click link
        img_thumb.click()
        
        # Reparse the website
        html = browser.html
        img_soup = soup(html, 'html.parser')
        
        # navigate full-image
        image = img_soup.find('li').find('a')
        image = image.get('href')
        img_url = f'{url}{image}'
        
        # get title
        img_title = img_soup.find('h2', class_="title").get_text()
            
        # Add to list
        hemispheres['img_url'] = img_url
        hemispheres['title'] = img_title
        
        # naviagte back to links
        browser.back()
        
        hemisphere_image_urls.append(hemispheres)

    # 4. Print the list that holds the dictionary of each image url and title.
    hemisphere_image_urls

    # 5. Quit the browser
    browser.quit()

    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())