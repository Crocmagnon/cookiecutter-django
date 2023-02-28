# {{cookiecutter.project_name}}

## Quick start
Clone, then
```shell
pip install -U pip pip-tools invoke
inv sync-dependencies
pre-commit install --install-hooks
inv test
./src/manage.py migrate
./src/manage.py createsuperuser
```

# Reuse
If you do reuse my work, please consider linking back to this repository 🙂
