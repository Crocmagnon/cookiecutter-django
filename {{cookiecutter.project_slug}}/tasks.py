import time
from pathlib import Path

from invoke import task

BASE_DIR = Path(__file__).parent.resolve(strict=True)
SRC_DIR = BASE_DIR / "src"
COMPOSE_BUILD_FILE = BASE_DIR / "docker-compose-build.yaml"
COMPOSE_BUILD_ENV = {"COMPOSE_FILE": COMPOSE_BUILD_FILE}
TEST_ENV = {"ENV_FILE": BASE_DIR / "envs" / "test-envs.env"}


@task
def update_dependencies(ctx):
    common_args = "-q --allow-unsafe --resolver=backtracking --upgrade"
    with ctx.cd(BASE_DIR):
        ctx.run(
            f"pip-compile {common_args} --generate-hashes requirements.in",
            pty=True,
            echo=True,
        )
        ctx.run(
            f"pip-compile {common_args} --strip-extras -o constraints.txt requirements.in",
            pty=True,
            echo=True,
        )
        ctx.run(
            f"pip-compile {common_args} --generate-hashes requirements-dev.in",
            pty=True,
            echo=True,
        )
        ctx.run("pip-sync requirements.txt requirements-dev.txt", pty=True, echo=True)


@task
def makemessages(ctx):
    with ctx.cd(SRC_DIR):
        ctx.run("./manage.py makemessages -l en -l fr", pty=True, echo=True)


@task
def compilemessages(ctx):
    with ctx.cd(SRC_DIR):
        ctx.run("./manage.py compilemessages -l en -l fr", pty=True, echo=True)


@task
def test(ctx):
    with ctx.cd(SRC_DIR):
        ctx.run("pytest", pty=True, echo=True, env=TEST_ENV)


@task
def test_cov(ctx):
    with ctx.cd(SRC_DIR):
        ctx.run(
            "pytest --cov=. --cov-branch --cov-report term-missing:skip-covered",
            pty=True,
            echo=True,
            env={"COVERAGE_FILE": BASE_DIR / ".coverage"},
        )


@task
def pre_commit(ctx):
    with ctx.cd(BASE_DIR):
        ctx.run("pre-commit run --all-files", pty=True)


@task(pre=[pre_commit, test_cov])
def check(ctx):
    pass


@task
def build(ctx):
    with ctx.cd(BASE_DIR):
        ctx.run(
            "docker-compose build django", pty=True, echo=True, env=COMPOSE_BUILD_ENV
        )


@task
def publish(ctx):
    with ctx.cd(BASE_DIR):
        ctx.run(
            "docker-compose push django", pty=True, echo=True, env=COMPOSE_BUILD_ENV
        )


@task
def deploy(ctx):
    ctx.run("ssh ubuntu /mnt/data/checkout/update", pty=True, echo=True)


@task
def check_alive(ctx):
    import requests

    exception = None
    for _ in range(5):
        try:
            res = requests.get("https://{{cookiecutter.project_slug}}.augendre.info")
            res.raise_for_status()
            print("Server is up & running")
            return
        except requests.exceptions.HTTPError as e:
            time.sleep(2)
            exception = e
    raise RuntimeError("Failed to reach the server") from exception


@task(pre=[check, build, publish, deploy], post=[check_alive])
def beam(ctx):
    pass


@task
def download_db(ctx):
    with ctx.cd(BASE_DIR):
        ctx.run("scp ubuntu:/mnt/data/{{cookiecutter.project_slug}}/db/db.sqlite3 ./db/db.sqlite3")
        ctx.run("rm -rf src/media/")
        ctx.run("scp -r ubuntu:/mnt/data/{{cookiecutter.project_slug}}/media/ ./src/media")
    with ctx.cd(SRC_DIR):
        ctx.run("./manage.py changepassword gaugendre", pty=True)
