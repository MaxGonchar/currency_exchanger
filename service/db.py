import os


class DB:

    def __init__(self, db_name, path=None, db_file_extension='json'):
        self.path = path or os.getcwd()
        self.db_name = db_name
        self.db_file_extension = db_file_extension

    def init_db(self):
        db_path = self._get_db_path()
        if not os.path.isdir(db_path):
            os.mkdir(db_path)

    def get_all_db_files(self):
        all_files = os.listdir(self._get_db_path())
        db_files = filter(self._is_db_file, all_files)
        return list(db_files)

    def get_file_content(self, file_name):
        with open(self._det_file_path(file_name), 'r') as file:
            content = file.read()
        return content

    def create_file(self, file_name, content):
        with open(self._det_file_path(file_name), 'w') as file:
            file.write(content)

    def update_file(self, file_name, content):
        if os.path.isfile(self._det_file_path(file_name)):
            self.create_file(file_name, content)

    def delete_file(self, file_name):
        os.remove(self._det_file_path(file_name))

    def _get_db_path(self):
        return os.path.join(self.path, self.db_name)

    def _is_db_file(self, file_path):
        file, extension = os.path.splitext(file_path)
        return extension == f'.{self.db_file_extension}'

    def _det_file_path(self, file_name):
        return os.path.join(
            self._get_db_path(), f'{file_name}.{self.db_file_extension}'
        )


if __name__ == '__main__':
    # path = './'
    db_name = 'currency_exchanger_db_test'
    db = DB(db_name)

    # ----- TEST init_db -----
    # print(db.path)
    # db.init_db()

    # ----- TEST get_all_files -----
    # print(db.get_all_db_files())

    # ----- TEST get_file_content -----
    # print(db.get_file_content('1'))

    # ----- TEST create_file -----
    # content = '{"qwe": "asd"}'
    # db.create_file('new_file', content)

    # ----- TEST update_file -----
    # import json
    # file_name = 'new_file'
    # content = json.loads(db.get_file_content(file_name))
    # content.update({'1': '2'})
    # db.update_file(file_name, json.dumps(content))

    # ----- TEST delete_file -----
    # file_name = 'new_file'
    # db.delete_file(file_name)



