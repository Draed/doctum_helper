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

class TagCompleter(Completer):
    def __init__(self, base_directory):
        self.base_directory = os.path.abspath(base_directory)
        self.directory_names = self.get_directory_names()

    def get_directory_names(self):
        """Get a list of all directory names in the specified path and its subdirectories."""
        dir_names = []
        for root, dirs, _ in os.walk(self.base_directory):
            dir_names.extend(dirs)
        return dir_names

    def get_completions(self, document, complete_event):
        """Provide completions based on the current input."""
        text = document.text_before_cursor.strip()
        segments = text.split(',')
        if segments:
            last_segment = segments[-1].strip()
            for dir_name in self.directory_names:
                if dir_name.startswith(last_segment):
                    yield Completion(dir_name, start_position=-len(last_segment))

class ListCompleter(Completer):
    def __init__(self, items):
        self.items = items

    def get_completions(self, document, complete_event):
        """Provide completions based on the current input."""
        text = document.text_before_cursor.strip()
        for item in self.items:
            if item.startswith(text):
                yield Completion(item, start_position=-len(text))



