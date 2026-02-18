from setuptools import setup

setup(
    name="wit",
    version="0.1",
    # The source Python modules live in WitProject/src as top-level modules (cli.py, new.py, ui.py, core.py)
    py_modules=["cli", "new", "ui", "core"],
    package_dir={"": "WitProject/src"},
    install_requires=[
        "click>=8.0",
    ],
    entry_points={
        "console_scripts": [
            "wit=cli:main",  # 호출 מפונקציית main() בקובץ cli.py
        ],
    },
    python_requires=">=3.8",
)
