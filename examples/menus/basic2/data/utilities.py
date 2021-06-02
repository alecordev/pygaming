import os
import shutil


def clean_files():
    """remove all pyc files and __pycache__ direcetories in subdirectory"""
    for root, dirs, files in os.walk("."):
        for dir in dirs:
            if dir == "__pycache__":
                path = os.path.join(root, dir)
                print("removing {}".format(path))
                shutil.rmtree(path)
        for name in files:
            if name.endswith(".pyc"):
                path = os.path.join(root, name)
                print("removing {}".format(path))
                os.remove(path)
