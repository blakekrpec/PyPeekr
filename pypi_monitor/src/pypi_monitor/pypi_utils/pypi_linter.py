import subprocess


def linter():
    subprocess.run(["flake8", "pypi_monitor"])
