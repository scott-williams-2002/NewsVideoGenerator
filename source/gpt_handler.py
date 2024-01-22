from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import tqdm
from scraper import get_urls_from_google,get_images, get_article_text, is_text_accessible
from GPT_Wrapper import GPT_Wrapper



# generates the formatted gpt prompt for filtering headlines
def get_filter_prompt(research_question, headlines_and_urls):
    return [
        {"role": "system", "content": "You are a researcher who determines if news articles are good sources for a research topic based on the article's headline. If you are given a research topic, and a series of headlines, determine which 3 headlines and links are useful and not useful in a json format. DO NOT MAKE ANY FALSE INFORMATION. YOU ALWAYS TELL THE TRUTH. YOU ARE LOOKING FOR HIGHLY RELATED ARTICLE HEADLINES ONLY."},
        {"role": "user", "content": f"Here is the research question: {research_question}. Determine if these headlines are useful or not useful in researching the given topic. Here are the headlines and urls which appear in the format of a list of dictionaries with entries called 'title' and 'link' which correspond to the headline and url respectively: {headlines_and_urls}"}
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
        {"role": "system", "content": "You are a researcher and you job is to read articles, which have some messy sections due to copying and pasting them, and summarize the most important and controvertial points that would relate to a research question. This summary should be no longer than 3 sentences and should only gather the most important details that seem unique and non-general. Try to source important metrics, names, and places from the article. YOU NEVER make up information and you make sure to include the article's source and approximate publication date in the summary under the category 'citation' using this format: [Source: NewsPaper Times, May 2023]. Have one json category called 'summary' and one called 'citation'. YOU ALWAYS TELL FACTS. DO NOT MAKE ANYTHING UP."},
        {"role": "user", "content": f"Here is the research question: {research_question}. Write a detailed and concise summary of the following article and do not make up information or include any non-essential words: {article_text}. "}
    ]
#formatted gpt prompt to take summarized articles and make an article
def get_article_writer_prompt(research_question, summaries):
    #example script in another python file going to come up with alternative solution but good enough for now
    return [
        {"role": "system", "content": f"You are a writer who creates scripts based on a series of summarized news articles in an investigative style for short form content in videos that should not last longer than 40 seconds. Try to make the script captivating by using wording that is somewhat controversial. Using the following article summaries, write a short form video script (that should be around 40 seconds in length) that discusses the video's topic which will be given. The article summaries will appear in a json format with the summary and source. If you use information from one of the summaries, make sure to include a statement like this: 'according to The New York Times...'. The script should be outputted in a json format with paragraphs under a 'part' category and accompanying image or video suggestions under a 'visual' category name. NEVER MAKE ANY INFORMATION UP. MAKE THE SCRIPT LENGTH FOR A VIDEO WHICH IS LESS THAN ONE MINUTE. DO NOT LIE. ALL NEWS INCLUDED IN THE SCRIPT SHOULD BE SOURCED FROM THE SUMMARIES GIVEN."},
        {"role": "user", "content": f"The article summaries are here:{summaries}. Write a short form video script with the following topic: {research_question}"}
    ]
#returns only useful headlines and urls as a list of dictionaries
def filter_headlines(headlines_and_urls, research_question):
    model = GPT_Wrapper()
    prompt = get_filter_prompt(headlines_and_urls=headlines_and_urls, research_question=research_question)
    model_output = model.model_call_json(prompt=prompt, temp=0)
    return model_output['useful_headlines'] #returns only the useful_headlines section of json, which has url included with each headline

#generates possible google search querys based on research question
def generate_query(research_question, num_questions):
    model = GPT_Wrapper()
    prompt = get_query_prompt(research_question=research_question, num_questions=num_questions)
    model_output = model.model_call_json(prompt=prompt, temp=0.7)
    return list(model_output['queries'])

#given a research question and url, the model returns a 3 sentence summary that includes only the main points and date of publication if possible
def summarize_article(research_question, url):
    article_text = str(get_article_text(URL=url))
    prompt = get_summary_prompt(research_question=research_question, article_text=article_text)
    model = GPT_Wrapper()
    model_output = model.model_call_json(prompt=prompt, temp = 0.1)
    return model_output
    #might make sense to return model output as json rather than text block
    
#returns a large string formatted with all summaries found from a given google query list
def get_summaries_from_queries(queries, research_question):
    summaries = ''''''
    for query in tqdm.tqdm(queries): #tqdm iterator for progress bar since this takes a while
        headlines_and_urls_google = get_urls_from_google(query=query)
        useful_headlines = filter_headlines(headlines_and_urls=headlines_and_urls_google, research_question=research_question)
        print(f'\nSummarizing {len(useful_headlines)} articles for the query: {query}')
        for article in useful_headlines:
            if is_text_accessible(article['link']): #checks if text can be obtained from url to avoid calling gpt with no article text
                summary = summarize_article(research_question=research_question, url= article['link'])
                summaries += str(summary)
                summaries += "\n"
        os.system('cls' if os.name == 'nt' else 'clear') #clears the previous progress bar
        
    return summaries #returns a large string of summaries and citations for articles found using all queries


def generate_article(all_summaries, research_question):
    prompt = get_article_writer_prompt(research_question=research_question, summaries=all_summaries)
    model = GPT_Wrapper()
    model_output = model.model_call_json(prompt=prompt, temp=0.15)
    return model_output
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
    #make seperate audio files spliced together for different times to include images or videos using googlecloudapi



#print(generate_query("Who is really responsible for the 2008 financial crisis?", 15))
'''
print("\n")
query = "border crossings"
googled = get_urls_from_google(query=query)
titles = [googled_info['title'] for googled_info in googled]
links = [googled_info['link'] for googled_info in googled]

filtered = filter_headlines(links, titles, research_question="What is the impact of the undocumented immigrants entering the US from the southern border")
print(filtered)'''

#summarize_article(url="https://www.forbes.com/sites/richardnieva/2023/12/20/google-on-trial-2023/?sh=3227d7b97662", research_question="what are some issues with large tech companies?")

'''
Need to add RSG / vector embedding instead of summarize to get better contents
    - first take all of the article text and save as a large list for the research question
    - find a way to separate these contents into chunks and embed them as vectors
    - find the k closest/most similar vectors and use their contents in article writer prompt
        - can also have seperately engineered prompts for sections of generated script to reduce halucination and have more control over the style
    - when using the vector indices, which correspond to text and sources, reference the sources in script somehow
'''