import os
import shutil
from pathlib import Path
import hashlib
import time

def file_hash(path):
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

class WitManager:
    def __init__(self, path):
        self.working_path = Path(path).absolute()
        self.wit_path = self.working_path / ".wit"
        self.temp_dir = self.wit_path / "temp"
        self.commit_dir = self.wit_path / "commits"

    def init(self):
        os.makedirs(self.wit_path, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.commit_dir, exist_ok=True)
        print(f"Initialized .wit at {self.wit_path}")

    def get_witignore(self):
        ignored = [".wit"]
        ignore_file = self.working_path / ".witignore"
        if ignore_file.exists():  # ← שינוי קריטי: בדיקה אם הקובץ קיים
            with open(ignore_file, "r") as f:
                ignored += [line.strip() for line in f if line.strip()]
        return ignored

    def add(self, path="."):
        ignored_items = self.get_witignore()
        os.makedirs(self.temp_dir, exist_ok=True)

        paths_to_add = [self.working_path / p for p in os.listdir(self.working_path)
                        if path == "." and p not in ignored_items] \
                       if path == "." else [self.working_path / path]

        for src in paths_to_add:
            if not src.exists():  # ← שינוי קריטי: מניעת קריסה אם הקובץ/תיקייה לא קיימים
                print(f"Error: {src} not found")
                continue
            dst = self.temp_dir / src.name
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            elif src.is_file():
                shutil.copy2(src, dst)

    def commit(self, message):
        commit_id = hashlib.sha1(f"{time.time()}{message}".encode()).hexdigest()[:10]
        last_commit = self.get_last_commit_path()
        if last_commit and self.compare_folders(last_commit, self.temp_dir):  # ← שינוי קריטי: לא ליצור commit ללא שינוי
            print("No changes detected since last commit.")
            return

        new_commit_path = self.commit_dir / commit_id
        shutil.copytree(self.temp_dir, new_commit_path)
        with open(self.wit_path / "HEAD", "w") as f:
            f.write(commit_id)
        print(f"Commit {commit_id} created successfully.")

    def get_last_commit_path(self):
        head_file = self.wit_path / "HEAD"
        if not head_file.exists():  # ← שינוי קריטי: אם אין HEAD, מחזיר None
            return None
        last_id = head_file.read_text().strip()
        return self.commit_dir / last_id

    def compare_folders(self, folder1, folder2):
        folder1_files = [p.relative_to(folder1) for p in folder1.rglob("*") if p.is_file()]
        folder2_files = [p.relative_to(folder2) for p in folder2.rglob("*") if p.is_file()]
        if set(folder1_files) != set(folder2_files):  # ← שינוי קריטי: השוואת רשימות במקום סתם בדיקה של אורך
            return False
        for f in folder1_files:
            if file_hash(folder1 / f) != file_hash(folder2 / f):
                return False
        return True

    def checkout(self, commit_id):
        target = self.commit_dir / commit_id
        last_commit = self.get_last_commit_path()

        if self.temp_dir.exists() and (not last_commit or not self.compare_folders(last_commit, self.temp_dir)):  # ← שינוי קריטי: מניעת checkout עם uncommitted changes
            print("Error: You have uncommitted changes. Commit before checkout.")
            return
        if not target.exists():  # ← שינוי קריטי: בדיקה אם הקומיט קיים
            print(f"Error: Commit {commit_id} not found.")
            return

        # ניקוי working directory
        for item in self.working_path.iterdir():
            if item.name == ".wit":
                continue
            if item.is_file():
                item.unlink()
            else:
                shutil.rmtree(item)

        # העתקת commit ל-working directory
        for item in target.iterdir():
            if item.is_file():
                shutil.copy(item, self.working_path)
            else:
                shutil.copytree(item, self.working_path / item.name)

        # עדכון staging
        if self.temp_dir.exists():  # ← שינוי קריטי: מחיקת temp אם קיים לפני העתקת commit
            shutil.rmtree(self.temp_dir)
        shutil.copytree(target, self.temp_dir)

        print(f"Checked out commit {commit_id}")
def status(self):
    ignored_items = self.get_witignore()
    last_commit_path = self.get_last_commit_path()

    # כל הקבצים ב-temp (staging)
    staged_files = [p.relative_to(self.temp_dir) for p in self.temp_dir.rglob("*") if p.is_file() and p.name not in ignored_items]

    # אם אין staging ואין שינוי מאז הקומיט האחרון
    if not staged_files and (last_commit_path is None or self.compare_folders(last_commit_path, self.temp_dir)):
        return "nothing to commit, working tree clean"

    # יש קבצים ב-staging ושונה מהקומיט האחרון
    if staged_files and (last_commit_path is None or not self.compare_folders(last_commit_path, self.temp_dir)):
        return f"Changes to be committed: {[str(f) for f in staged_files]}"

    # בדיקה של קבצים ששונו ב-working אבל לא ב-staging
    modified_files = []
    for f in self.working_path.rglob("*"):
        if f.is_file() and f.name not in ignored_items:
            staged_file = self.temp_dir / f.relative_to(self.working_path)
            if staged_file.exists() and file_hash(f) != file_hash(staged_file):
                modified_files.append(str(f.relative_to(self.working_path)))

    if modified_files:
        return f"Changes not staged for commit: {modified_files}"

    return "No changes tracked"
