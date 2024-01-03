import os
import json
from GPT_Wrapper import GPT_Wrapper 

#saves json formatted video script contents
def save_script_as_json(script, file_name):
    new_dir_path = os.path.abspath("output_video_scripts")
    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)
    #checks if filename already in use and prompts overwrite or rename option
    file_name_path = os.path.join(new_dir_path, file_name)
    if os.path.exists(file_name_path):
        print(f"A file called {file_name} already exists")
        delete_file = input(f"Do you wish to overwrite {file_name} (y/n): ")
        # if user says yes delete old file
        if delete_file.lower() == "y":
            os.remove(file_name_path)
        #if user doesn't say yes ask for new file name
        else:
            new_file_name = input("Enter a new json file name to write to: ")
            file_name_path = os.path.join(new_dir_path, new_file_name)

    output_content = json.dumps(script, indent=len(script)) #formats to have propper indents for easier visualization
    
    #writes to file with specified criteria
    with open(file_name_path, "w") as out:
        out.write(output_content)
        print(f"json content written to '{file_name_path}'")



