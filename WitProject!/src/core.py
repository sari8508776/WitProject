import os
import shutil
from pathlib import Path
import hashlib
import time
"""
import os
import shutil
from pathlib import Path
import hashlib



class WitManager:
    id_dir=0
    def __init__(self, path):
        self.working_path = Path(path)
        self.wit_path = self.working_path / ".wit"
        os.system(f'attrib +h ".wit"')
        self.temp_dir=os.path.join(wit_path, "temp")
        self.commit_dir = os.path.join(wit_path, "commit")
        os.system(f'attrib +h "{commit}"')

    def init(self):
        os.makedirs(self.wit_path, exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        print(f"Initialized .wit at {self.wit_path}")

    def add(self,path):
        ignored_items = [".wit", ".witignore"]
        if path==".":
          for item in os.listdir(self.working_path):
             if  item not in ignored_items:
                source_path = os.path.join(self.working_path, item)
                destination_path = os.path.join(self.temp_dir, item)

                if os.path.isdir(source_path):
                    shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(source_path, destination_path)
        else:
            source_path = os.path.join(self.working_path, item)
            destination_path = os.path.join(self.temp_dir, item)
            if os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
            else:
                shutil.copy2(source_path, destination_path)
            print(f"Added {path} to staging area.")

def commit(message):
    wit_manager = WitManager(working_path)
    if os.path.exists(wit_manager.commit_dir):
       print(f"Committing to {wit_manager.commit_dir}")#יש להוסיף שגיאה!
    if not id_dir == 0:
        commit_folder = working_path / f"commit{id_dir}"
        if compare_folders(commit_folder, self.temp_dir):
            print(f"Commit folder {commit_folder} already exists.")#יש להוסיף שגיאה!
        else:
            id_dir += 1
            os.commit_folder.join(wit_path, f"commit{id_dir}")
            current=commit_folder / f"commit{id_dir}"
            shutil.rmtree(self.temp_dir)
            os.mkdir(self.temp_dir)
    shutil.copytree(self.temp_dir, current, dirs_exist_ok=True)


def file_hash(path):
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def compare_folders(folder1_path, folder2_path):
    folder1 = Path(folder1_path)
    folder2 = Path(folder2_path)

    for file1 in folder1.rglob("*"):  # מעבר על כל הקבצים והתיקיות בתיקייה הראשונה (כולל תתי-תיקיות)
        if file1.is_file():  # בדיקה שהאובייקט הוא קובץ ולא תיקייה
            relative = file1.relative_to(folder1)  # יצירת נתיב יחסי ביחס לתיקייה הראשונה
            file2 = folder2 / relative  # יצירת הנתיב המקביל בתיקייה השנייה

            # if not file2.exists():  # בדיקה אם הקובץ לא קיים בתיקייה השנייה
            #     print("❌ חסר בתיקייה השנייה:", relative)  # הדפסת הודעה על קובץ חסר

           if  file_hash(file1) != file_hash(file2):
               return False

    return True
#############################
import os
import shutil
import hashlib
from pathlib import Path

class WitManager:
    id_dir = 0

    def __init__(self, path):
        self.working_path = Path(path)
        self.wit_path = self.working_path / ".wit"
        self.temp_dir = self.wit_path / "temp"
        self.commit_dir = self.wit_path / "commit"

    def init(self):
        os.makedirs(self.wit_path, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.commit_dir, exist_ok=True)
        if os.name == "nt":
            os.system(f'attrib +h "{self.wit_path}"')
            os.system(f'attrib +h "{self.commit_dir}"')
            os.system(f'attrib +h "{self.temp_dir}"')
        print(f"Initialized .wit at {self.wit_path}")

    def add(self, path="."):
        ignored_items = [".wit", ".witignore"]
        if path == ".":
            for item in os.listdir(self.working_path):
                if item not in ignored_items:
                    source_path = self.working_path / item
                    destination_path = self.temp_dir / item
                    if source_path.is_dir():
                        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
                    else:
                        shutil.copy2(source_path, destination_path)
        else:
            source_path = self.working_path / path
            destination_path = self.temp_dir / path
            if source_path.is_dir():
                shutil.copytree(source_path, destination_path, dirs_exist_o


"""



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
        if os.name == 'nt':
            os.system(f'attrib +h "{self.wit_path}"')
        print(f"Initialized .wit at {self.wit_path}")

    def add(self, path_str):
        ignored_items = [".wit", ".witignore"]
        os.makedirs(self.temp_dir, exist_ok=True)
        if path_str == ".":
            for item in os.listdir(self.working_path):
                if item not in ignored_items:
                    self._do_copy(self.working_path / item)
        else:
            self._do_copy(self.working_path / path_str)

    def _do_copy(self, source):
        if not source.exists():
            print(f"Error: {source} not found")
            return
        destination = self.temp_dir / source.name
        if source.is_dir():
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(source, destination)

    def commit(self, message):
        commit_id = hashlib.sha1(f"{time.time()}{message}".encode()).hexdigest()[:10]
        new_commit_path = self.commit_dir / commit_id
        last_commit_path = self.get_last_commit_path()
        if last_commit_path and self.compare_folders(last_commit_path, self.temp_dir):
            print("No changes detected since last commit.")
            return

        shutil.copytree(self.temp_dir, new_commit_path)
        with open(self.wit_path / "HEAD", "w") as f:
            f.write(commit_id)
        print(f"Commit {commit_id} created successfully.")

    def get_last_commit_path(self):
        head_file = self.wit_path / "HEAD"
        if not head_file.exists():
            return None
        with open(head_file, "r") as f:
            last_id = f.read().strip()
            return self.commit_dir / last_id

    def compare_folders(self, folder1, folder2):
        files1 = list(folder1.rglob("*"))
        files2 = list(folder2.rglob("*"))
        if len(files1) != len(files2): return False
        for f1 in files1:
            if f1.is_file():
                relative = f1.relative_to(folder1)
                f2 = folder2 / relative
                if not f2.exists() or file_hash(f1) != file_hash(f2):
                    return False
        return True


def file_hash(path):
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def status(self):
    ignored_items = [".wit", ".witignore"]
    last_commit_path = self.get_last_commit_path()

    if not any(self.temp_dir.iterdir()) and (
            last_commit_path is None or self.compare_folders(last_commit_path, self.temp_dir)):
        return "nothing to commit, working tree clean"

    else:
        if any(self.temp_dir.iterdir()) and (
                last_commit_path is None or not self.compare_folders(last_commit_path, self.temp_dir)):
            list_files1 = [item for item in os.listdir(self.temp_dir) if item not in ignored_items]
            return f"Changes to be committed: {list_files1}"

        else:
            if not self.compare_folders(self.working_path, self.temp_dir):
                list_files2 = [item for item in os.listdir(self.working_path) if item not in ignored_items]
                return f"Changes not staged for commit: {list_files2}"

    return "No changes tracked"


def checkout(self, commit_id):
    target_commit_path = self.commit_dir / commit_id

    if not target_commit_path.exists():
        print(f"Error: Commit {commit_id} not found.")
        return

    for item in self.working_path.iterdir():
        if item.name == ".wit":
            continue
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

    for item in target_commit_path.iterdir():
        if item.is_file():
            shutil.copy(item, self.working_path)
        elif item.is_dir():
            shutil.copytree(item, self.working_path / item.name)

    shutil.rmtree(self.temp_dir)
    shutil.copytree(target_commit_path, self.temp_dir)

    print(f"Checked out commit {commit_id}")















