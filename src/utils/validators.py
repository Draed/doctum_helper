import os

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