from gpt_handler import *
from scraper import get_urls_from_google
import time
from os import get_terminal_size
import sys
import tqdm

def main():
    #first call generate queries with inputted research question
    research_question = str(input("Enter a video topic/ research question: "))
    queries = generate_query(research_question=research_question, num_questions=5)
    
    #then get urls
    summaries = get_summaries_from_queries(queries=queries, research_question=research_question)

    print(summaries)



        
        

if __name__ == "__main__":
    main()