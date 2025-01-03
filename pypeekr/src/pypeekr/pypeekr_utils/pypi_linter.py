import subprocess


def linter():
    subprocess.run(["flake8", "pyseekr"], check=False)
