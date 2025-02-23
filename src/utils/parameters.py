import json
import os
import inquirer

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter

from utils.validators import integer_validate, null_validate
from utils.git_utils import set_git_config

config_file = './config.json'

def edit_parameters(term):
    params = {}
    completer = PathCompleter()
    session = PromptSession(completer=completer)
    ## doctum_path
    params['doctum_path'] = session.prompt("Enter the path for doctum_content: ", completer=completer)
    ## default_doctum_vars
    doctum_default_questions = [
        inquirer.Text('default_doctum_duration', message="Enter the course default duration (in minutes)", validate=integer_validate),
        inquirer.List('default_doctum_complexity', message="Enter the course default difficulty",choices=["low", "medium", "high"]),
        inquirer.Text('default_doctum_task_duration', message="Enter the course default TASK duration (in minutes)",validate=integer_validate),
        inquirer.Confirm('default_doctum_git_feature', message="Should git feature be activated ?",default=True),
    ]
    doctum_answers = inquirer.prompt(doctum_default_questions)
    ## default doctum git vars
    if doctum_answers['default_doctum_git_feature']:
        doctum_default_git_questions = [
            inquirer.Text('default_doctum_repo_path', message="Enter doctum_content repository path", default=os.path.dirname(params['doctum_path']), validate=null_validate),
            inquirer.Text('default_doctum_remote_name', message="Enter the doctum_content remote name", default="origin", validate=null_validate),
            inquirer.Text('default_doctum_branch_name', message="Enter the docum_content branch name",default="main", validate=null_validate),
            inquirer.Text('default_doctum_git_username', message="Enter the docum_content git username",default="doctum_helper", validate=null_validate),
            inquirer.Text('default_doctum_git_email', message="Enter the docum_content git email",default="docutm_helper@mail.local", validate=null_validate),
        ]
        doctum_git_answers = inquirer.prompt(doctum_default_git_questions)
        
        params['default_doctum_repo_path'] = doctum_git_answers['default_doctum_repo_path']
        params['default_doctum_remote_name'] = doctum_git_answers['default_doctum_remote_name']
        params['default_doctum_branch_name'] = doctum_git_answers['default_doctum_branch_name']
        params['default_doctum_git_username'] = doctum_git_answers['default_doctum_git_username']
        params['default_doctum_git_email'] = doctum_git_answers['default_doctum_git_email']

        set_git_config(term, params['default_doctum_repo_path'], params['default_doctum_git_username'], params['default_doctum_git_email'])

    params['default_doctum_git_feature'] = doctum_answers['default_doctum_git_feature']
    params['default_doctum_duration'] = doctum_answers['default_doctum_duration']
    params['default_doctum_complexity'] = doctum_answers['default_doctum_complexity']
    params['default_doctum_task_duration'] = doctum_answers['default_doctum_task_duration']




    params['default_doctum_task_description'] = []
    while True:
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

def get_parameters(term):
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            params = json.load(file)
            return params
    else:
        params = edit_parameters(term)
        return params
