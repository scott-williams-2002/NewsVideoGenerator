from dotenv import load_dotenv
import os
from openai import OpenAI
import json
from scraper import get_urls_from_google,get_images

load_dotenv()

#returns only useful headlines and urls as a list of dictionaries
def filter_headlines(urls, headlines, research_question):
    #in json mmode, pass in headlines with associated urls and ask to seperate them into useful or nonuseful urls/headlines based on headline in json format
    client = OpenAI()
    # gpt call 
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={ "type": "json_object" },
    temperature = 0,
    messages=[
        {"role": "system", "content": "You are a researcher who determines if news articles are good sources for a research topic based on the article's headline. If you are given a research topic, and a series of headlines, determine which headlines and links are useful and not useful in a json format. DO NOT MAKE ANY FALSE INFORMATION. YOU ALWAYS TELL THE TRUTH. YOU ARE LOOKING FOR HIGHLY RELATED ARTICLE HEADLINES ONLY."},
        {"role": "user", "content": f"Here is the research question: {research_question}. Determine if these headlines are useful or not useful in researching the given topic. Here are the headlines seperated by commas: {headlines}. In the same ordering, the associated headline urls are here:{urls}"}
    ])
    model_output = json.loads((response.choices[0].message.content))
    #result = [{'headline': model_output['title'], 'url': model_output['link']} for model_output['title'], model_output['link'] in zip(model_output['title'], model_output['link'])]
    return model_output['useful_headlines']



query = "border crossings"
googled = get_urls_from_google(query=query)
titles = [googled_info['title'] for googled_info in googled]
links = [googled_info['link'] for googled_info in googled]

filtered = filter_headlines(links, titles, research_question="What is the impact of the undocumented immigrants entering the US from the southern border")
print(filtered)

#next make a function to call the get related urls and then check again if their headlines are useful
def get_all_urls():
    pass
    # first load list of possible searches for google from research question which can be generated by chat gpt
    #then get all the urls and check for relevance
        #if some are releavant, look for other urls found on those relevant ones
        #enter infinite while loop to get desired amount of useful articles

def generate_article():
    pass
    #summarize each article into three sentences (can be passed in by function)
    # put all together into new api call to make an article (use prompt engineering to make it more captivating: "you are a news/story writer make a captingvtnng story about this research topic")
    # after put together, should have another engineered prompt to act as discriminator, checking it against another type of script like jake tran's style of script
        #this descriminator should be engineered aswell to act as an editor
    # loop until the discriminator likes the script

def add_images():
    pass
    # given an article written, and some image descriptions, which can be another function that uses vision api
    # find locations where it would be relevant to add in the image we found
    # can return script with "image one here" text or something like tha
    # or a json file which says which images to include in which order