from dotenv import load_dotenv
import os
from openai import OpenAI
import json
from scraper import get_urls_from_google,get_images, get_article_text
from GPT_Wrapper import GPT_Wrapper


# generates the formatted gpt prompt for filtering headlines
def get_filter_prompt(research_question, headlines, urls):
    return [
        {"role": "system", "content": "You are a researcher who determines if news articles are good sources for a research topic based on the article's headline. If you are given a research topic, and a series of headlines, determine which headlines and links are useful and not useful in a json format. DO NOT MAKE ANY FALSE INFORMATION. YOU ALWAYS TELL THE TRUTH. YOU ARE LOOKING FOR HIGHLY RELATED ARTICLE HEADLINES ONLY."},
        {"role": "user", "content": f"Here is the research question: {research_question}. Determine if these headlines are useful or not useful in researching the given topic. Here are the headlines seperated by commas: {headlines}. In the same ordering, the associated headline urls are here:{urls}"}
    ]
#generates the formatted gpt prompt for query generation
def get_query_prompt(research_question, num_questions):
    return [
        {"role": "system", "content": "You are a researcher who is great at taking research questions, and creating the best google searches to source information to answer the research question"},
        {"role": "user", "content": f"Here is the research question: {research_question}. Write {str(num_questions)} google search queries which will help find sources for a news article which answers the research question. Return the searches in a json format using the key 'queries'."}
    ]
#generates the formatted gpt prompt for summarizing article text
def get_summary_prompt(research_question, article_text):
    return [
        {"role": "system", "content": "You are a researcher and you job is to read articles, which have some messy sections due to copying and pasting them, and summarize the most important and controvertial points that would relate to a research question. This summary should be no longer than 3 sentences and should only gather the most important details. YOU never make up information and you make sure to include the article's source and approximate publication date in the summary also in this format: [Source: NewsPaper Times, 2023]. YOU ALWAYS TELL FACTS. DO NOT MAKE ANYTHING UP."},
        {"role": "user", "content": f"Here is the research question: {research_question}. Write a detailed and concise summary of the following article and do not make up information or include any non-essential words: {article_text}. "}
    ]

#returns only useful headlines and urls as a list of dictionaries
def filter_headlines(urls, headlines, research_question):
    model = GPT_Wrapper()
    prompt = get_filter_prompt(urls=urls, headlines=headlines, research_question=research_question)
    model_output = model.model_call_json(prompt=prompt, temp=0)
    return model_output['useful_headlines'] #returns only the useful_headlines section of json, which has url included with each headline

#generates possible google search querys based on research question
def generate_query(research_question, num_questions):
    model = GPT_Wrapper()
    prompt = get_query_prompt(research_question=research_question, num_questions=num_questions)
    model_output = model.model_call_json(prompt=prompt, temp=0.3)
    return list(model_output['queries'])

#given a research question and url, the model returns a 3 sentence summary that includes only the main points and date of publication if possible
def summarize_article(research_question, url):
    article_text = str(get_article_text(URL=url))
    prompt = get_summary_prompt(research_question=research_question, article_text=article_text)
    model = GPT_Wrapper()
    model_output = model.model_call_text(prompt=prompt, temp = 0.1)
    print(model_output)
    


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


#print(generate_query("Who is really responsible for the 2008 financial crisis?", 15))
'''
print("\n")
query = "border crossings"
googled = get_urls_from_google(query=query)
titles = [googled_info['title'] for googled_info in googled]
links = [googled_info['link'] for googled_info in googled]

filtered = filter_headlines(links, titles, research_question="What is the impact of the undocumented immigrants entering the US from the southern border")
print(filtered)'''

summarize_article(url="https://www.forbes.com/sites/richardnieva/2023/12/20/google-on-trial-2023/?sh=3227d7b97662", research_question="how do sports and school coexist?")