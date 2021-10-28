from unittest.mock import patch

import pytest

from service.db import DB, DBErrors


@patch('service.db.os.path')
@patch('service.db.os')
def test_init_db_success(mock_os, mock_path):
    test_db = DB('test_db', 'some_path')
    mock_path.join.return_value = 'some_path/test_db'
    mock_path.isdir.return_value = False
    test_db.init_db()
    mock_os.mkdir.assert_called_with('some_path/test_db')


@patch('service.db.os')
@patch('service.db.os.path')
def test_init_db_already_exists(mock_path, mock_os):
    test_db = DB('test_db', 'some_path')
    mock_path.join.return_value = 'some_path/test_db'
    mock_path.isdir.return_value = True
    mock_os.mkdir.side_effect = FileExistsError(
        "File exists: 'some_path/test_db'"
    )
    with pytest.raises(DBErrors) as error:
        test_db.init_db()
    assert error.value.reason == 'Data Base error'
    assert str(error.value.message) == "File exists: 'some_path/test_db'"


def test_get_all_db_files_success(tmpdir):
    mock_dir = tmpdir.mkdir('test_db')
    mock_dir.join('file1.json').write({1: 1})
    mock_dir.join('file2.json').write({1: 1})
    mock_dir.join('file3.txt').write('{1:1}')
    mock_dir.join('file4.txt').write('{1:1}')
    test_db = DB('test_db', tmpdir.strpath)
    files = test_db.get_all_db_files()
    assert ('file1.json' in files) and ('file2.json' in files)
    assert ('file3.txt' not in files) and ('file4.txt' not in files)


if __name__ == '__main__':
    pytest.main()
