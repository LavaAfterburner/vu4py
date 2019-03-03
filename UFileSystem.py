
from vu4py.ULogger import ULogger
import os
import shutil


class UFileSystem:
    class FileBatch:
        def __init__(self, root_dir, start_depth=0, end_depth=-1):
            self.root_dir = root_dir
            self.start_depth = start_depth
            self.end_depth = end_depth

            self.files = list()
            self.folders = list()

        def collect_batch(self, collect_files=True, collect_folders=True):
            if UFileSystem.Settings.LOG_INFO:
                ULogger.log("Collecting FileBatch from {}".format(self.root_dir))
            for root, dirs, files in os.walk(self.root_dir, ):
                depth = len(root.split(UFileSystem.Settings.SLASH))

                if collect_files:
                    for name in files:
                        if depth > self.start_depth and (depth < self.end_depth or self.end_depth == -1):
                            self.files.append((root + UFileSystem.Settings.SLASH + name, name), root)
                if collect_folders:
                    for name in dirs:
                        if depth > self.start_depth and (depth < self.end_depth or self.end_depth == -1):
                            self.folders.append((root + UFileSystem.Settings.SLASH + name, name), root)

        def collapse_folders(self, rename_func):
            if UFileSystem.Settings.LOG_INFO:
                print()
                ULogger.log("Collapsing Folder Structure")

            if UFileSystem.Settings.LOG_INFO and self.end_depth != -1:
                ULogger.log("As end_depth does not == -1: Errors may occur", ULogger.Levels.WARNING)

            if UFileSystem.Settings.LOG_INFO:
                ULogger.log("Moving Files")
            for file in self.files:
                new_name = file[1]
                if rename_func is not None:
                    new_name = rename_func(file[0], file[1])

                os.rename(file[0], self.root_dir + UFileSystem.Settings.SLASH + new_name)

            if UFileSystem.Settings.LOG_INFO:
                ULogger.log("Deleting Folders")
            for folder in self.folders[::-1]:
                os.remove(folder[0])
                self.folders.remove(folder)

        def move_to(self, dest):
            if UFileSystem.Settings.LOG_INFO:
                print()
                ULogger.log("Moving FileBatch to " + dest)

            if UFileSystem.Settings.LOG_INFO and self.end_depth != -1:
                ULogger.log("As end_depth does not == -1: more files could be moved", ULogger.Levels.WARNING)

            if UFileSystem.Settings.LOG_INFO:
                ULogger.log("Finding Root Folders to move")
            folders_to_move = [name for name in os.listdir(self.root_dir)
                               if os.path.isdir(self.root_dir + UFileSystem.Settings.SLASH + name)]
            if UFileSystem.Settings.LOG_INFO:
                ULogger.log("Moving Folders")
            for folder in folders_to_move:
                shutil.move(self.root_dir + UFileSystem.Settings.SLASH + folder, dest)

        def rename_files(self, rename_func):
            for file in self.files:
                new_name = rename_func(file[0], file[1])
                os.rename(file[0], file[2] + UFileSystem.Settings.SLASH + new_name)

        def rename_folders(self, rename_func):
            for folder in self.folders:
                new_name = rename_func(folder[0], folder[1])
                os.rename(folder[0], folder[2] + UFileSystem.Settings.SLASH + new_name)

        def __str__(self):
            return "FileBatch\n" \
                   "=========\n" \
                   "Files: " + str(self.files) + "\n" \
                   "Folders: " + str(self.folders)

    class Settings:
        LOG_INFO = False
        SLASH = "\\"

    class FolderBlueprint:
        def __init__(self, root_dir, structure):
            """
            Stores a Structure of Folders

            :param root_dir: The root directory of the Folder Structure
            :type root_dir: str
            :param structure: Dictionary containing the Structure
            :type structure: dict
            """
            self.root_dir = root_dir
            self.structure = structure

        def create_structure(self):
            """
            Creates the given structure of folders the root_dir
            :return: None
            """

            def check(obj, parent):
                if not type(obj) is dict:
                    return
                for key in obj.keys():
                    name = parent + UFileSystem.Settings.SLASH + key
                    folders.append(name)
                    check(obj[key], name)

            folders = list()

            if UFileSystem.Settings.LOG_INFO:
                print()
                ULogger.log("Analysing Structure")

            check(self.structure, self.root_dir)

            if UFileSystem.Settings.LOG_INFO:
                ULogger.log("Making Structure")
            for folder in folders:
                os.makedirs(folder, exist_ok=True)
                if UFileSystem.Settings.LOG_INFO:
                    ULogger.log(" - " + folder)
            if UFileSystem.Settings.LOG_INFO:
                ULogger.log(" > Complete")

        def __str__(self):
            return str(self.structure)
