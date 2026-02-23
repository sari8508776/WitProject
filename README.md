# Wit (mini-wit)

Short: Minimal version control tool (init, add, commit, status, checkout).

Requirements
- Python 3.8+
- Install dependencies:
pip install -r requirements.txt

Installation (Development)
1. Create a virtual environment and activate (PowerShell):
.\venv\Scripts\Activate.ps1
2. Install dependencies:
pip install -r requirements.txt
3. For local installation for convenience (generates a CLI command named `wit` on the system):
pip install -e .

Project structure

- `src/` — CLI source code and logic (`cli.py`, `new.py`, `ui.py`, `core.py`).

Usage
- CLI commands are accessible as `wit` command if you have installed the package; Otherwise run the module directly `python -m cli ...` (or `python -m src.cli ...` depending on the location of the files).

Commands and examples (Windows PowerShell)

1) Initialize a repository in the current directory
```bash
wit init
```
- Creates the system's internal data structures (metadata sections, etc.).

2) Add files to the staging area
```bash
wit add file1.txt
wit add dir\subfile.txt
```
- Adds files to be identified for the next commit (based on the logic in `new.py`).

3) Make a commit
```bash
wit commit -m "Initial commit"
```
- Saves a snapshot of the files you added. The output prints a commit id.
Example output:
```
Committed 1 files
Commit id: 9f2b1a3
```

4) Check status
```bash
wit status
```
- Shows changed files, new files, and the status against the last head/commit.

5) checkout (restore file from commit)
```bash
wit checkout 9f2b1a3 -- file1.txt
```
- Returns file1.txt to its state as it was in the commit with id 9f2b1a3.

Example of a full script

1. Boot:
```bash
wit init
```

2. Add + commit:
```bash
echo Hello > file1.txt
wit add file1.txt
wit commit -m "Add file1"
```

=> Commit id: abcdef1

3. Change + status + commit:
"""PowerShell"""
```bash
Add-Content -Path file1.txt -Value "Update"
wit status
wit add file1.txt
wit commit -m "Update file1"
```
"""

4. Rollback:
```bash
wit checkout abcdef1 -- file1.txt
```

Additional notes
- Make sure the `.witignore` file (if present) is set as desired to prevent unwanted files from being tracked.
- If the CLI is not available as a `wit` command, the module can be run directly from src according to the file organization: `python -m cli init`.

If If you wish, I can adjust the README according to the exact layout (are the files under a `wit` package in `src/` or as modules in the root of `src/`) and provide more actual output examples.
