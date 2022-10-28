import os


COMMANDS_TO_RUN = [
    "poetry install",
    "pre-commit install",
    "pre-commit autoupdate",
    "pre-commit run --all-files",
    "git add poetry.lock",
    "git commit -m 'Add poetry lock file'",
    "pycharm .",
    "./src/manage.py migrate",
    "./src/manage.py createcachetable",
    "./src/manage.py createsuperuser",
    "./src/manage.py runserver",
]

def main():
    os.system("git init")
    os.system("git add .")
    os.system("git commit -m 'Initial commit'")
    os.system("pyenv virtualenv {{cookiecutter.python_version}} {{cookiecutter.project_slug}}")
    os.system("pyenv local {{cookiecutter.project_slug}}")
    print("\nWe created a virtualenv using {{cookiecutter.python_version}} for you.")
    print("Run the following commands:")
    print("cd {{cookiecutter.project_slug}} && direnv allow")
    print(" && ".join(COMMANDS_TO_RUN))


if __name__ == '__main__':
    main()
