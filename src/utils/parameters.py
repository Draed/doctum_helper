import json
import os
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter

config_file = './config.json'

def edit_parameters():

    params = {}
    completer = PathCompleter()
    session = PromptSession(completer=completer)
    params['doctum_path'] = session.prompt("Enter the path for doctum_content: ", completer=completer)
    with open(config_file, 'w') as file:
        json.dump(params, file)
    
    return params

def get_parameters():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            params = json.load(file)
            return params
    else:
        params = edit_parameters()
        return params
