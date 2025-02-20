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
            directory = os.path.join(self.base_directory, text)
        
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.startswith(os.path.basename(text)):
                    yield Completion(filename, start_position=-len(text))

# Create a PromptSession
session = PromptSession()

