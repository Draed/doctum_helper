from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
import os

class RelativePathCompleter(Completer):
    def __init__(self, base_directory):
        self.base_directory = os.path.abspath(base_directory)

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if not text:
            directory = self.base_directory
        else:
            if os.path.isabs(text):
                return

            if not text.startswith(('/', './')):
                text = os.path.join(self.base_directory, text)
            
            ## Split the input into directory and file name and convert to absolute path
            directory, _, _ = text.rpartition('/')
            directory = os.path.abspath(directory)
        
        try:
            if os.path.exists(directory):
                ## List directories in the specified directory
                for entry in os.listdir(directory):
                    full_path = os.path.join(directory, entry)
                    ## Only suggest directories
                    if os.path.isdir(full_path) and entry.startswith(os.path.basename(text)):
                        yield Completion(entry, start_position=-len(text))
        except FileNotFoundError:
            pass

session = PromptSession()

