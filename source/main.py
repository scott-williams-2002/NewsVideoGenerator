from gpt_handler import *
from scraper import get_urls_from_google, get_article_text
import time
import sys
import tqdm
from TTS_Wrapper import TTS_Wrapper
from Editor_Model import Editor_Model
from data_storage import *

def main():
    '''
    #first call generate queries with inputted research question
    script_name = str(input("Enter a title for this script: "))
    research_question = str(input("Enter a video topic/ research question: "))
    queries = generate_query(research_question=research_question, num_questions=5)
    
    #then get urls
    summaries = get_summaries_from_queries(queries=queries, research_question=research_question)
    article_json = generate_article(all_summaries=summaries, research_question=research_question)

    #save script to file
    save_script_as_json(article_json, script_name= script_name)
    '''

    article_json = get_json_contents(script_name="iran_news")
    script_text_only = ' '.join(article_json['part'])
    print(script_text_only)
    tts = TTS_Wrapper()
    tts.set_audio_config()
    tts.set_voice()
    tts.generate_speech(script_text_only)
    tts.write_to_file(file_name="republican.mp3")
    

   

if __name__ == "__main__":
    main()
    