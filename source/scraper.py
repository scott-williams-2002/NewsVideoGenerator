import requests
from bs4 import BeautifulSoup
import requests, json, lxml


#returns a list of lines of the article
def get_article_text(URL):
    # Send an HTTP GET request to the URL
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml')
    all_text = ""
    # Find news articles using article tags or other relevant tags
    for p_element in soup.find_all('p'):
        all_text += p_element.text
    return all_text
    
    

# based on a url passed in, a list of urls that are within than webpage is returned if any
def find_related_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    related_urls = []
    for link in soup.find_all('a'):
        related_urls.append(link.get('href'))
    cleaned_list=[i for i in related_urls if i]
    cleaned_list = set(cleaned_list)
    return list(cleaned_list)

# given a url, a list of all images and their alt descriptions is returned as 2 objects seperately
def get_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all images on the page.
    images = soup.find_all('img')
    # Get the urls of the images.
    image_urls = [image['src'] for image in images]
    image_descriptions = [image['alt'].encode(encoding="utf-8") for image in images]
    if len(image_urls) == 0:
        return None
    return image_urls, image_descriptions

#given a string query, and some device browser information, a google search url is constructed with urls related to the desired topic
def get_urls_from_google(query):
  page_limit = 10          
  page_num = 0
  data = []
  params = {"q": query, "hl": "en", "gl": "us", "start": 0}

  headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"}

  while True:
    page_num += 1
    html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(html.text, 'lxml')
    #dont understand this stuff but helps get links associated
    for result in soup.select(".tF2Cxc"):
        title = result.select_one(".DKV0Md").text
        links = result.select_one(".yuRUbf a")["href"] 
        #appends the assicated data in a json format
        data.append({
          "title": title,
          "link": links,
        })
    # stop loop due to page limit condition
    if page_num == page_limit:
        break
    # stop the loop on the absence of the next page
    if soup.select_one(".d6cvqb a[id=pnnext]"):
        params["start"] += 10
    else:
        break
  return data

#given a url, checks if it is possible to obtain raw text
def is_text_accessible(url):
    #call get text method and check output
    test_text = get_article_text(url)

    if test_text == None:
        return False
    elif len(test_text) == 0:
        return False
    else: 
        return True