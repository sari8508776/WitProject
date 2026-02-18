import os
import shutil
from pathlib import Path
import hashlib
import time
import json
from datetime import datetime
import unicodedata

# =================== פונקציות עזר ===================
def file_hash(path):
    """Calculate MD5 hash of a file"""
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def normalize_path(path):
    """Normalize path string to remove invisible RTL characters"""
    return unicodedata.normalize("NFC", str(path)).replace("\u200f", "").replace("\u202b", "")

# helper to check ignored paths
def _is_ignored(rel_path, ignored_items):
    """Return True if rel_path (Path or str) should be ignored based on ignored_items list.

    This does a simple check: if the top-level name or the full relative string equals
    any ignore entry, it is considered ignored. This keeps behavior simple and predictable
    for the assignment requirements.
    """
    rp = str(rel_path).replace("\\", "/")
    parts = rp.split("/") if rp else []
    top = parts[0] if parts else rp
    for ig in ignored_items:
        if not ig:
            continue
        igs = ig.replace("\\", "/")
        if igs == top or igs == rp:
            return True
    return False

# =================== מחלקת WitManager ===================
class WitManager:
    def __init__(self, path):
        self.working_path = Path(path).absolute()
        self.wit_path = self.working_path / ".wit"
        self.temp_dir = self.wit_path / "temp"
        self.commit_dir = self.wit_path / "commits"

    # ---------- Init ----------
    def init(self):
        os.makedirs(self.wit_path, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.commit_dir, exist_ok=True)
        print(f"Initialized .wit at {self.wit_path}")

    # ---------- Witignore ----------
    def get_witignore(self):
        ignored = [".wit"]
        ignore_file = self.working_path / ".witignore"
        if ignore_file.exists():
            with open(ignore_file, "r") as f:
                ignored += [line.strip() for line in f if line.strip()]
        return ignored

    # ---------- Add ----------
    def add(self, path="."):
        """Add files to staging (temp).

        Behavior changes:
        - If path == '.' we recreate staging from the current working tree while
          honoring .witignore entries (so ignored files won't be staged).
        - If a specific path is given, it's added/updated in staging.
        """
        ignored_items = self.get_witignore()

        if path == ".":
            # Recreate staging to reflect current working tree (excluding ignored)
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
            os.makedirs(self.temp_dir, exist_ok=True)

            for p in self.working_path.rglob("*"):
                if not p.is_file():
                    continue
                rel = p.relative_to(self.working_path)
                if _is_ignored(rel, ignored_items):
                    continue
                dst = self.temp_dir / normalize_path(str(rel))
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dst)
        else:
            src = self.working_path / path
            if not src.exists():
                print(f"Error: {src} not found")
                return
            os.makedirs(self.temp_dir, exist_ok=True)
            dst = self.temp_dir / normalize_path(src.name)
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

    # ---------- Commit ----------
    def commit(self, message):
        commit_id = hashlib.sha1(f"{time.time()}{message}".encode()).hexdigest()[:10]
        last_commit = self.get_last_commit_path()

        # אם אין שינויים מאז הקומיט האחרון – עצירה
        if last_commit and self.compare_folders(last_commit, self.temp_dir):
            print("No changes detected since last commit.")
            return

        new_commit_path = self.commit_dir / commit_id
        os.makedirs(new_commit_path, exist_ok=True)

        # העתקת הקבצים מ-temp לקומיט החדש עם נירמול השמות
        for src in self.temp_dir.rglob("*"):
            rel_path = src.relative_to(self.temp_dir)
            dst = new_commit_path / normalize_path(str(rel_path))
            if src.is_dir():
                os.makedirs(dst, exist_ok=True)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

        # שמירת metadata
        metadata = {
            "id": commit_id,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        with open(new_commit_path / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        # עדכון HEAD
        with open(self.wit_path / "HEAD", "w", encoding="utf-8") as f:
            f.write(commit_id)

        # ריענון staging
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        shutil.copytree(new_commit_path, self.temp_dir)

        print(f"Commit {commit_id} created successfully.")

    # ---------- Last Commit Path ----------
    def get_last_commit_path(self):
        head_file = self.wit_path / "HEAD"
        if not head_file.exists():
            return None
        last_id = head_file.read_text().strip()
        return self.commit_dir / last_id

    # ---------- Compare Folders ----------
    def compare_folders(self, folder1, folder2):
        folder1_files = [normalize_path(p.relative_to(folder1)) for p in folder1.rglob("*") if p.is_file()]
        folder2_files = [normalize_path(p.relative_to(folder2)) for p in folder2.rglob("*") if p.is_file()]
        if set(folder1_files) != set(folder2_files):
            return False
        for f in folder1_files:
            file1 = folder1 / f
            file2 = folder2 / f
            if file_hash(file1) != file_hash(file2):
                return False
        return True

    # ---------- Checkout ----------
    def checkout(self, commit_id):
        target = self.commit_dir / commit_id
        if not target.exists():
            print(f"Error: Commit {commit_id} not found.")
            return False

        ignored_items = self.get_witignore()

        # Block checkout אם יש שינויים לא מועלים ב-working directory לעומת staging
        if self.temp_dir.exists():
            for p in self.working_path.rglob("*"):
                if not p.is_file():
                    continue
                rel = p.relative_to(self.working_path)
                if _is_ignored(rel, ignored_items):
                    continue
                staged_file = self.temp_dir / rel
                if staged_file.exists() and file_hash(p) != file_hash(staged_file):
                    print("Error: You have uncommitted changes. Commit before checkout.")
                    return False

        # ניקוי working directory מכל הקבצים (חוץ מ-.wit)
        for item in self.working_path.iterdir():
            if item.name == ".wit":
                continue
            if item.is_file():
                item.unlink()
            else:
                shutil.rmtree(item)

        # העתקת כל הקבצים מהקומיט המבוקש ל-working directory
        for src in target.rglob("*"):
            rel = src.relative_to(target)
            if src.is_file():
                dst = self.working_path / normalize_path(rel)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            elif src.is_dir():
                dst = self.working_path / normalize_path(rel)
                dst.mkdir(parents=True, exist_ok=True)

        # ריענון staging כדי שישקף את הקומיט החדש
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        shutil.copytree(target, self.temp_dir)

        print(f"Checked out commit {commit_id}")
        return True

    """
    def checkout(self, commit_id):
        target = self.commit_dir / commit_id
        last_commit = self.get_last_commit_path()

        # Block checkout if there are uncommitted changes in the working tree.
        # We'll compare the working tree (excluding ignored files) with the staging area.
        ignored_items = self.get_witignore()
        if self.temp_dir.exists():
            # gather working files (relative) excluding ignored
            working_files = [p.relative_to(self.working_path) for p in self.working_path.rglob("*") if p.is_file() and not _is_ignored(p.relative_to(self.working_path), ignored_items)]
            staged_files = [p.relative_to(self.temp_dir) for p in self.temp_dir.rglob("*") if p.is_file() and p.name != "metadata.json"]
            # normalize sets
            wf_set = set(normalize_path(str(p)) for p in working_files)
            sf_set = set(normalize_path(str(p)) for p in staged_files)
            # if any file set differs OR any shared file has different content -> uncommitted changes
            if wf_set != sf_set:
                print("Error: You have uncommitted changes. Commit before checkout.")
                return False
            else:
                # check content equality
                for rel in wf_set:
                    wpath = self.working_path / rel
                    spath = self.temp_dir / rel
                    if not spath.exists() or file_hash(wpath) != file_hash(spath):
                        print("Error: You have uncommitted changes. Commit before checkout.")
                        return False

        if not target.exists():
            print(f"Error: Commit {commit_id} not found.")
            return False

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
            dest = self.working_path / normalize_path(item.name)
            if item.is_file():
                shutil.copy2(item, dest)
            else:
                shutil.copytree(item, dest, dirs_exist_ok=True)

        # ריענון staging
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        shutil.copytree(target, self.temp_dir)

        print(f"Checked out commit {commit_id}")
        return True


"""

    # ---------- Status ----------
    def status(self):
        ignored_items = self.get_witignore()
        last_commit_path = self.get_last_commit_path()

        # קבצים ב-temp (staging) - למעט metadata.json
        staged_files = [normalize_path(p.relative_to(self.temp_dir)) for p in self.temp_dir.rglob("*") if p.is_file() and p.name != "metadata.json" and not _is_ignored(p.relative_to(self.temp_dir), ignored_items)] if self.temp_dir.exists() else []

        # כל הקבצים ב-working directory (למעט ignored)
        all_files = [normalize_path(p.relative_to(self.working_path)) for p in self.working_path.rglob("*") if p.is_file() and not _is_ignored(p.relative_to(self.working_path), ignored_items)]

        # קבצים שנמצאים בקומיט אחר
        committed_files = []
        if last_commit_path and last_commit_path.exists():
            committed_files = [normalize_path(p.relative_to(last_commit_path)) for p in last_commit_path.rglob("*") if p.is_file() and p.name != "metadata.json" and not _is_ignored(p.relative_to(last_commit_path), ignored_items)]

        # קבצים לא ב-staging ולא בקומיט
        untracked_files = [str(f) for f in all_files if f not in staged_files and f not in committed_files]

        # קבצים ששונו ב-working אבל לא ב-staging
        modified_files = []
        for f in all_files:
            staged_file = self.temp_dir / f
            working_file = self.working_path / f
            if staged_file.exists() and file_hash(working_file) != file_hash(staged_file):
                modified_files.append(str(f))

        result = []
        if staged_files:
            result.append(f"Changes to be committed: {[str(f) for f in staged_files]}")
        if modified_files:
            result.append(f"Changes not staged for commit: {modified_files}")
        if untracked_files:
            result.append(f"Untracked files: {untracked_files}")
        if not result:
            result.append("nothing to commit, working tree clean")
        return "\n".join(result)
