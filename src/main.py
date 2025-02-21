import json
import os
import datetime
import inquirer

from blessed import Terminal
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter

from utils.completers import RelativePathCompleter
from utils.parameters import get_parameters, edit_parameters
from utils.validators import is_valid_json_path, null_validate

## Get parameters
parameters = get_parameters()
default_doctum_path = parameters['doctum_path']

## Initialize blessed terminal
term = Terminal()

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
    session = PromptSession(completer=completer, complete_while_typing=True)

    ## json file question
    json_file_path_question = session.prompt(
        f"Enter the path for the new new doctum course [suggestions from {default_doctum_path}]: ",
        completer=completer
    )
    json_file_path = f"{default_doctum_path}/{json_file_path_question}"

    ## json file answer validation
    if not is_valid_json_path(term, json_file_path):
        return

    ## Create the directory path if it does not exist
    directory = os.path.dirname(json_file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(term.green(f"Created directory: {directory}"))

    
    ## default values
    default_doctum_duration = 60
    default_doctum_complexity = "medium"
    default_doctum_date = datetime.datetime.now().isoformat()

    ## main doctum data questions
    doctum_questions = [
        inquirer.Text('doctum_name', message="Enter the course name", validate=null_validate),
        inquirer.Text('doctum_description', message="Enter the course description", validate=null_validate),
        inquirer.Text('doctum_duration', message="Enter the course estimated duration (in minutes)", default=default_doctum_duration, validate=null_validate),
        inquirer.Text('doctum_difficulty', message="Enter the course estimated difficulty (low, medium, high)", default=default_doctum_complexity, validate=null_validate),
        inquirer.Text('doctum_date_added', message="Enter the added date (YYYY-MM-DD)", default=default_doctum_date, validate=null_validate),
        inquirer.Text('doctum_tags', message="Enter tags (comma-separated)", validate=null_validate)
    ]
    doctum_answers = inquirer.prompt(doctum_questions)

    data = {}
    data['name'] = doctum_answers['doctum_name']
    data['description'] = doctum_answers['doctum_description']
    data['estimated_duration'] = doctum_answers['doctum_duration']
    data['difficulty'] = doctum_answers['doctum_difficulty']
    data['added_date'] = doctum_answers['doctum_date_added']
    data['tags'] = [tag.strip() for tag in doctum_answers['doctum_tags'].split(',')]
    
    ## tasks questions
    data['task_list'] = []
    print(term.blue("Doctum task definition"))
    task_id=0
    while True:
        print(term.grey(task_data) for task_data in data['task_list'])
        main_task_question = [
            inquirer.Confirm("add_task", message="Adding a new task",default=False)
        ]
        main_task_answers = inquirer.prompt(main_task_question)

        if main_task_answers['add_task']: 
            task_id = task_id + 1
            ## task description
            task_description = input(term.green("    Enter task description: "))
            if not task_description:
                print(term.red("    Task description cannot be empty. Please try again."))
                continue
            ## task duration
            task_duration = input(term.green("    Enter task duration (in minutes): "))
            if not task_duration:
                print(term.red("    Task duration cannot be empty. Please try again."))
                continue
            
            data['task_list'].append({
                "id": task_id,
                "description": task_description,
                "duration": task_duration
            })
        else:
            break
        
    ## achieve
    while True:
        achieved_input = input(term.green("Is it achieved? (true/false): ")).lower()
        if achieved_input in ['true', 'false']:
            data['achieved'] = achieved_input == 'true'
            break
        else:
            print(term.red("    Please enter 'true' or 'false'."))

    ## Create the JSON file
    try:
        with open(json_file_path, 'w') as json_file:
            json.dump([data], json_file, indent=4)
        print(term.green(f"JSON file created at: {json_file_path}"))
    except Exception as e:
        print(term.red(f"Error creating JSON file: {e}"))

def show_parameters():
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
    main()
