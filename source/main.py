from gpt_handler import *
from scraper import get_urls_from_google, get_article_text
import time
from os import get_terminal_size
import sys
import tqdm
from TTS_Wrapper import TTS_Wrapper
from Editor_Model import Editor_Model

def main():
    #first call generate queries with inputted research question
    research_question = str(input("Enter a video topic/ research question: "))
    queries = generate_query(research_question=research_question, num_questions=5)
    
    #then get urls
    summaries = get_summaries_from_queries(queries=queries, research_question=research_question)
    article_json = generate_article(all_summaries=summaries, research_question=research_question)

    

    
    #script_text_only = ''.join(article_json['part'])
    #tts = TTS_Wrapper()
    #tts.set_audio_config()
    #tts.set_voice()
    #tts.generate_speech(script_text_only)
    #tts.write_to_file(file_name="republican.mp3")
    

   

if __name__ == "__main__":
    main()
    