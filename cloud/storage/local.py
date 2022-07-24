import os
import shutil
from typing import List

from .basic import CloudStorage


class LocalStorageException(Exception):
    pass


class Storage(CloudStorage):
    """ Storage class for local environment """

    def load_file(self, file_path: str) -> bytes:
        with open(file_path, "rb") as f:
            file = f.read()
        return file

    def save_file(self, file_obj: bytes, path: str) -> None:
        with open(path, "wb") as f:
            f.write(file_obj)

    def list_files(self, path: str) -> List[str]:
        if os.path.isfile(path):
            raise LocalStorageException(f"{path} is a file not dir.")
        return os.listdir(path)

    def copy_file(self, file_path: str, destination: str) -> None:
        shutil.copy(file_path, destination)

    def delete(self, path: str) -> None:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    def move_file(self, file_path, destination):
        shutil.move(file_path, destination)

    def create_folder(self, name: str, path: str) -> None:
        os.mkdir(os.path.join(path, name))
