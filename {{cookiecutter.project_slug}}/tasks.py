from pathlib import Path

from invoke import Context, task

BASE_DIR = Path(__file__).parent.resolve(strict=True)
SRC_DIR = BASE_DIR / "src"
COMPOSE_BUILD_FILE = BASE_DIR / "docker-compose-build.yaml"
COMPOSE_BUILD_ENV = {"COMPOSE_FILE": COMPOSE_BUILD_FILE}
TEST_ENV = {"ENV_FILE": BASE_DIR / "envs" / "test-envs.env"}


@task
def sync_dependencies(ctx: Context, *, update: bool = False):
    common_args = "-q --allow-unsafe --resolver=backtracking"
    if update:
        common_args += " --upgrade"
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
def update_dependencies(ctx: Context):
    return sync_dependencies(ctx, update=True)


@task
def makemessages(ctx: Context):
    with ctx.cd(SRC_DIR):
        ctx.run("./manage.py makemessages -l en -l fr", pty=True, echo=True)


@task
def compilemessages(ctx: Context):
    with ctx.cd(SRC_DIR):
        ctx.run("./manage.py compilemessages -l en -l fr", pty=True, echo=True)


@task
def test(ctx: Context):
    with ctx.cd(SRC_DIR):
        ctx.run("pytest", pty=True, echo=True, env=TEST_ENV)


@task
def test_cov(ctx: Context):
    with ctx.cd(SRC_DIR):
        ctx.run(
            "pytest --cov=. --cov-branch --cov-report term-missing:skip-covered",
            pty=True,
            echo=True,
            env={"COVERAGE_FILE": BASE_DIR / ".coverage"},
        )


@task
def download_db(ctx: Context):
    with ctx.cd(BASE_DIR):
        ctx.run("scp ubuntu:/mnt/data/{{cookiecutter.project_slug}}/db/db.sqlite3 ./db/db.sqlite3")
        ctx.run("rm -rf src/media/")
        ctx.run("scp -r ubuntu:/mnt/data/{{cookiecutter.project_slug}}/media/ ./src/media")
    with ctx.cd(SRC_DIR):
        ctx.run("./manage.py changepassword gaugendre", pty=True)
