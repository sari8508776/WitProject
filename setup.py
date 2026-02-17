from setuptools import setup, find_packages

setup(
    name="wit",
    version="0.1",
    packages=find_packages("WitProject/src"),  # חיפוש מודולים בתיקיית src
    package_dir={"": "WitProject/src"},        # src היא תיקיית הבסיס למודולים
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "wit=cli:main",  # main() בקובץ cli.py
        ],
    },
)
