from gpt_handler import *
from scraper import get_urls_from_google

def main():
    #first call generate queries with inputted research question
    research_question = str(input("Enter a video topic/ research question: "))
    queries = generate_query(research_question=research_question, num_questions=5)
    
    #then get urls
    headlines_and_urls_google = get_urls_from_google(query=queries[0])
    useful_headlines = filter_headlines(headlines_and_urls=headlines_and_urls_google, research_question=research_question)
    
    print(len(useful_headlines))
    
    for article in useful_headlines:
        summary = summarize_article(research_question=research_question, url= article['link'])
        print("-----------------")
        print(summary)




if __name__ == "__main__":
    main()