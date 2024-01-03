import os
import json
from GPT_Wrapper import GPT_Wrapper 

#saves json formatted video script contents
def save_script_as_json(script, script_name):
    script_name += ".json" #script name is just a string
    new_dir_path = os.path.abspath("output_video_scripts")
    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)
    #checks if filename already in use and prompts overwrite or rename option
    file_name_path = os.path.join(new_dir_path, script_name)
    if os.path.exists(file_name_path):
        print(f"A file called {script_name} already exists")
        delete_file = input(f"Do you wish to overwrite {script_name} (y/n): ")
        # if user says yes delete old file
        if delete_file.lower() == "y":
            os.remove(file_name_path)
        #if user doesn't say yes ask for new file name
        else:
            new_file_name = input("Enter a new json file name to write to (EX: FILE_NAME.json)): ")
            file_name_path = os.path.join(new_dir_path, new_file_name)

    output_content = json.dumps(script, indent=len(script)) #formats to have propper indents for easier visualization
    
    #writes to file with specified criteria
    with open(file_name_path, "w") as out:
        out.write(output_content)
        print(f"json content written to '{file_name_path}'")

#returns a json file's contents
def get_json_contents(script_name):
    script_name += ".json"
    dir_path = os.path.abspath("output_video_scripts")
    file_name_path = os.path.join(dir_path, script_name)

    #if file exists return the json object from file and if not return nothing
    if os.path.exists(file_name_path):
        with open(file_name_path, 'r') as json_file:
            json_object = json.load(json_file)
        return json_object
    return None
