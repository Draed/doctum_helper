import os
import re

from datetime import datetime
from inquirer import errors

def is_valid_json_path(term, file_path):
    """Check if the provided path is valid and ends with .json."""
    if not file_path.endswith('.json'):
        print(file_path)
        print(term.red("Error: The file path must end with '.json'."))
        return False
    # directory = os.path.dirname(file_path)
    # if directory and not os.path.exists(directory):
    #     print(term.red(f"Error: The directory '{directory}' does not exist."))
    #     return False
    return True


def null_validate(answers, current):
    if not current:
        raise errors.ValidationError('', reason=" Please enter a value")
    return True

def integer_validate(answers, current):
    if not current:
        raise errors.ValidationError('', reason=" Please enter a value")
    else:
        try:
            int(current)
            return True
        except ValueError:
            raise errors.ValidationError('', reason=" Pease enter an integer value")

def date_8601_validate(answers, current):
    if not current:
        raise errors.ValidationError('', reason=" Please enter a value")
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, current):
        raise errors.ValidationError('', reason=" Pease enter valid ISO 8601 date format")
    return True

def tag_validate(answers, current):
    pattern = r'^[a-zA-Z0-9]+(,[a-zA-Z0-9]+)*$'
    if not re.match(pattern, current):
        raise errors.ValidationError('', reason=" Pease enter valid tag string separate by comma")
    return True