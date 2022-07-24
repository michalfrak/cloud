from abc import ABC, abstractmethod


class CloudStorage(ABC):
    """ Abstract class with definitions of cloud provider storage """

    @abstractmethod
    def load_file(self, file_path):
        """ Load file from path """
        pass

    @abstractmethod
    def save_file(self, file_obj, path):
        """ Save file to path """
        pass

    @abstractmethod
    def list_files(self, path):
        """ List files from path """
        pass

    @abstractmethod
    def copy_file(self, file_path, destination):
        """ Copy file from path to destination """
        pass

    def delete(self, path):
        """ Delete file or folder """
        pass

    @abstractmethod
    def move_file(self, file_path, destination):
        """ Move file from path to destination """
        pass

    @abstractmethod
    def create_folder(self, name, path):
        """ Create folder in path """
        pass
