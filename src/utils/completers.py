from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
import os

class CustomPathCompleter(Completer):
    def __init__(self, base_directory):
        self.base_directory = base_directory

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        directory, _, _ = text.rpartition('/')
        
        if not directory:
            directory = self.base_directory
        
        # List files in the directory
        try:
            if os.path.commonpath([directory, self.base_directory]) == self.base_directory:
                for filename in os.listdir(directory):
                    if filename.startswith(os.path.basename(text)):
                        yield Completion(os.path.join(directory, filename), start_position=-len(text))
        except FileNotFoundError:
            pass

# Create a PromptSession
session = PromptSession()

