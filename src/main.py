import json
import os
import datetime
import inquirer

from blessed import Terminal
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter

from utils.completers import RelativePathCompleter, TagCompleter, ListCompleter
from utils.parameters import get_parameters, edit_parameters
from utils.validators import is_valid_json_path, null_validate, integer_validate, date_8601_validate, tag_validate

def display_menu():
    questions = [
        inquirer.List('action',
                      message="Please choose an option:",
                      choices=["Create doctum course", "Show parameters", "Edit parameters", "Exit"],
                      ),
    ]
    return inquirer.prompt(questions)['action']

def create_json_file():

    ## custom completer instanciation
    completer = RelativePathCompleter(base_directory=default_doctum_path)
    session = PromptSession(complete_while_typing=True)

    ## json file question
    while True:
        json_file_path_question = session.prompt(
            f"Enter the path for the new new doctum course [suggestions from {default_doctum_path}] \n(use tab for completion): ",
            completer=completer
        )
        
        # Check if the input corresponds to an existing file
        full_path = os.path.join(default_doctum_path, json_file_path_question)
        if os.path.isfile(full_path):
            print(term.red(f'Error: "{json_file_path_question}" already exist, please choose another name.'))
        else:
            break
    json_file_path = f"{default_doctum_path}/{json_file_path_question}"

    ## json file answer validation
    if not is_valid_json_path(term, json_file_path):
        return

    ## Create the directory path if it does not exist
    directory = os.path.dirname(json_file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(term.green(f"Created directory: {directory}"))

    ## default value for doctum_date_added (current date)
    default_doctum_date = datetime.datetime.now().strftime('%Y-%m-%d')

    ## main doctum data questions
    doctum_questions = [
        inquirer.Text('doctum_name', message="Enter the course name", validate=null_validate),
        inquirer.Text('doctum_description', message="Enter the course description", validate=null_validate),
        inquirer.Text('doctum_duration', message="Enter the course estimated duration (in minutes)", default=default_doctum_duration, validate=integer_validate),
        inquirer.List('doctum_difficulty', message="Enter the course estimated difficulty",choices=["low", "medium", "high"], default=default_doctum_complexity),
        inquirer.Text('doctum_date_added', message="Enter the added date (YYYY-MM-DD)", default=default_doctum_date, validate=date_8601_validate),
        # inquirer.Text('doctum_tags', message="Enter tags (comma-separated)", validate=tag_validate)
    ]
    doctum_answers = inquirer.prompt(doctum_questions)

    data = {}
    data['name'] = doctum_answers['doctum_name']
    data['description'] = doctum_answers['doctum_description']
    data['estimated_duration'] = doctum_answers['doctum_duration']
    data['difficulty'] = doctum_answers['doctum_difficulty']
    data['added_date'] = doctum_answers['doctum_date_added']
    
    ## tag question
    tag_completer = TagCompleter(base_directory=default_doctum_path)
    doctum_tags_question = session.prompt(
        "Enter tags (comma-separated) (use tab for completion): ",
        completer=tag_completer
    )
    data['tags'] = [tag.strip() for tag in doctum_tags_question.split(',') if tag.strip()]
    
    ## tasks questions
    data['task_list'] = []
    list_completer = ListCompleter(default_doctum_task_description)
    print(term.blue("Doctum task definition"))
    task_id=0
    while True:
        print(*[term.purple(json.dumps(task_data)) for task_data in data['task_list']])
        main_task_question = [
            inquirer.Confirm("add_task", message="Adding a new task",default=False)
        ]
        main_task_answers = inquirer.prompt(main_task_question)

        if main_task_answers['add_task']: 
            task_id = task_id + 1

            ## task description question (using completion)
            content_task_description = session.prompt(
                "Enter task description (use tab for completion): ",
                completer=list_completer
            )
            ## task duration question
            content_task_question = [
                inquirer.Text("task_duration", message="Enter task duration (in minutes)", default=default_doctum_duration, validate=integer_validate),
            ]
            content_task_answers = inquirer.prompt(content_task_question)
            data['task_list'].append({
                "id": task_id,
                "description": content_task_description,
                "duration": content_task_answers['task_duration']
            })
        else:
            break
        
    ## Achieved
    achieved_question = [
        inquirer.Confirm("achieved", message="Is doctum course already achieved/done ?",default=False)
    ]
    achieved_answer= inquirer.prompt(achieved_question)
    data['achieved'] = achieved_answer['achieved']

    ## Create the JSON file
    try:
        with open(json_file_path, 'w') as json_file:
            json.dump([data], json_file, indent=4)
        print(term.green(f"JSON file created at: {json_file_path}"))
    except Exception as e:
        print(term.red(f"Error creating JSON file: {e}"))

def show_parameters():
    parameters = get_parameters()
    for key, value in parameters.items():
        print(term.green(f"{key}: {value}"))

def main():
    while True:
        action = display_menu()
        
        if action == "Exit":
            print(term.red("Exiting the application."))
            break
        elif action == "Create doctum course":
            create_json_file()
        elif action == "Show parameters":
            show_parameters()
        elif action == "Edit parameters":
            edit_parameters()
            
if __name__ == "__main__":
    ## Get parameters
    parameters = get_parameters()
    default_doctum_path = parameters['doctum_path']
    default_doctum_duration = parameters['default_doctum_duration']
    default_doctum_complexity = parameters['default_doctum_complexity']
    default_doctum_task_description = parameters['default_doctum_task_description']

    ## Initialize blessed terminal
    term = Terminal()
    main()
