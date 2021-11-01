import os

from service.errors import DBErrors


def os_errors_catcher(method):
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except OSError as error:
            raise DBErrors(error)
    return wrapper


def decorate_cls_methods(decorator):
    """Decorate attributes of class which are callable by 'decorator'"""
    def class_wrapper(cls):
        for attr in cls.__dict__:

            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))

        return cls

    return class_wrapper


@decorate_cls_methods(os_errors_catcher)
class DB:
    """DB is a folder with files, where each file should be a model instance"""

    def __init__(
            self, db_name: str,  # db folder name
            path: str = None,  # path to db, default - app folder
            db_file_extension: str = 'json'
    ):
        self.path = path or os.getcwd()
        self.db_name = db_name
        self.db_file_extension = db_file_extension

    def init_db(self):
        """Create folder for db files"""
        db_path = self._get_db_path()
        if not os.path.isdir(db_path):
            os.mkdir(db_path)

    def get_all_db_files(self) -> list[str]:
        """Return list of file names
        with extension == self.db_file_extension"""
        all_files = os.listdir(self._get_db_path())
        db_files = filter(self._is_db_file, all_files)
        return list(db_files)

    def get_file_content(self, file_name: str) -> str:
        with open(self._get_file_path(file_name), 'r') as file:
            content = file.read()
        return content

    def create_file(self, file_name: str, content: str) -> None:
        with open(self._get_file_path(file_name), 'w') as file:
            file.write(content)

    def update_file(self, file_name: str, content: str) -> None:
        """Replace old file content with new"""
        if os.path.isfile(self._get_file_path(file_name)):
            self.create_file(file_name, content)

    def delete_file(self, file_name: str) -> None:
        os.remove(self._get_file_path(file_name))

    def _get_db_path(self) -> str:
        """Return path for db folder"""
        return os.path.join(self.path, self.db_name)

    def _is_db_file(self, file_path: str) -> bool:
        """
        Return True if file extension is equal to db files extension,
        or False if not
        """
        file, extension = os.path.splitext(file_path)
        return extension == f'.{self.db_file_extension}'

    def _get_file_path(self, file_name: str) -> str:
        """Return path to db file"""
        return os.path.join(
            self._get_db_path(), f'{file_name}.{self.db_file_extension}'
        )
