
import git
import os

def git_pull(term, repo_path, remote_name='origin', branch_name='main'):

    try:
        repo = git.Repo(repo_path)
        origin = repo.remote(name=remote_name)
        origin.pull(branch_name)
        print(term.green("git pull successfully."))
    except Exception as e:
        print(term.red(f"An error occurred while git pull : {e}"))

def set_git_config(term, repo_path, username, email):
    try:
        repo = git.Repo(repo_path)
        repo.config_writer().set_value("user", "name", username).release()
        repo.config_writer().set_value("user", "email", email).release()
        print(term.green("Git username and email set successfully."))

    except Exception as e:
        print(term.red(f"An error occurred while setting config: {e}"))

def git_commit_and_push(term, repo_path, commit_message, remote_name='origin', branch_name='main'):
    try:
        repo = git.Repo(repo_path)
        origin = repo.remote(name=remote_name)
        ## Stage all changes
        repo.git.add(A=True)
        repo.index.commit(commit_message)
        origin.push(branch_name)
        print(term.green("Changes committed and pushed successfully."))

    except Exception as e:
        print(term.red(f"An error occurred: {e}"))