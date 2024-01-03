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

    editor = Editor_Model()
    editor.edit_script(research_question=research_question, draft_script=article_json)

    print(editor.get_new_script())
    
    #script_text_only = ''.join(article_json['part'])
    #tts = TTS_Wrapper()
    #tts.set_audio_config()
    #tts.set_voice()
    #tts.generate_speech(script_text_only)
    #tts.write_to_file(file_name="republican.mp3")
    
def test():
    script = '''Narrator: "Hey there, dog lovers! Today, we're diving into the wonderful world of our furry friends and exploring some fascinating facts about dogs."

[FACT #1]
[Visual: Montage of different dog breeds]
Narrator: "Did you know that there are over 340 different dog breeds? From tiny Chihuahuas to majestic Great Danes, each one is unique and special."

[FACT #2]
[Visual: Cute puppy playing with a toy]
Narrator: "Puppies have 28 teeth, while adult dogs have 42! That's a lot of chewing power, perfect for those favorite toys."

[FACT #3]
[Visual: Slow-motion of a dog shaking off water]
Narrator: "Ever wondered why dogs shake off water after a bath? It's a natural instinct to dry off quickly and keep warm. Just one of the many quirky behaviors our canine companions have!"

[FACT #4]
[Visual: Dogs participating in various activities – running, playing fetch, swimming]
Narrator: "Dogs are not just pets; they're amazing athletes! Their incredible speed, agility, and endurance make them perfect companions for various activities, from running to playing fetch."

[CONCLUSION]
[Visual: A close-up of a dog with a heartwarming expression]
Narrator: "In less than a minute, we've only scratched the surface of the incredible world of dogs. Whether they're our loyal friends or working partners, one thing is for sure – dogs make our lives better in every way!"'''

    editor = Editor_Model()
    print(editor.edit_script(research_question="what are some facts about dogs", draft_script=script))

   

if __name__ == "__main__":
    test()
    