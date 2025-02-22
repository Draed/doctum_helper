import json
import os
import inquirer

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter

from utils.validators import integer_validate

config_file = './config.json'

def edit_parameters():
    params = {}
    completer = PathCompleter()
    session = PromptSession(completer=completer)
    ## doctum_path
    params['doctum_path'] = session.prompt("Enter the path for doctum_content: ", completer=completer)
    ## default_doctum_vars
    doctum_default_questions = [
        inquirer.Text('default_doctum_duration', message="Enter the course default duration (in minutes)", validate=integer_validate),
        inquirer.List('default_doctum_complexity', message="Enter the course default difficulty",choices=["low", "medium", "high"]),
    ]
    doctum_answers = inquirer.prompt(doctum_default_questions)
    params['default_doctum_duration'] = doctum_answers['default_doctum_duration']
    params['default_doctum_complexity'] = doctum_answers['default_doctum_complexity']
    params['default_doctum_task_description'] = []
    while True:
        # print(term.grey(task_data) for task_data in data['task_list'])
        main_task_question = [
            inquirer.Confirm("add_task", message="Adding a default description task for completion",default=False)
        ]
        main_task_answers = inquirer.prompt(main_task_question)

        if main_task_answers['add_task']: 
            doctum_default_task_questions = [
                inquirer.Text('default_doctum_task_description', message="Enter default task description")
            ]
            doctum_default_task_answers = inquirer.prompt(doctum_default_task_questions)

            params['default_doctum_task_description'].append(doctum_default_task_answers['default_doctum_task_description'])
        else:
            break

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
