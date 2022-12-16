# {{cookiecutter.project_slug}}

## Quick start
Clone, then
```shell
pyenv virtualenv {{cookiecutter.python_version}} {{cookiecutter.project_slug}}
pyenv local {{cookiecutter.project_slug}}
pip install pip-tools
pip-sync requirements.txt requirements-dev.txt
pre-commit install --install-hooks
inv test
./src/manage.py migrate
./src/manage.py createsuperuser
```
