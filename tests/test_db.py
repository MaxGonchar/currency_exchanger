import json
from unittest.mock import patch
from uuid import uuid4

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


@patch('service.db.os.path')
@patch('service.db.os')
def test_init_db_failed(mock_os, mock_path):
    test_db = DB('test_db', 'some_path')

    mock_path.join.return_value = 'some_path/test_db'
    mock_path.isdir.return_value = False
    mock_os.mkdir.side_effect = OSError(
        "Some OS Error during db_init"
    )

    with pytest.raises(DBErrors) as error:
        test_db.init_db()

    assert error.value.reason == 'Data Base error'
    assert str(error.value.message) == "Some OS Error during db_init"


@patch('service.db.os')
@patch('service.db.os.path')
def test_init_db_already_exists(mock_path, mock_os):
    test_db = DB('test_db', 'some_path')

    mock_path.join.return_value = 'some_path/test_db'
    mock_path.isdir.return_value = True

    test_db.init_db()

    mock_os.mkdir.assert_not_called()


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


@patch('service.db.os')
def test_get_all_db_files_failed(mock_os):
    mock_os.listdir.side_effect = OSError("Some OS Error during get_all_files")

    test_db = DB('test_db', 'test_path')

    with pytest.raises(DBErrors) as error:
        test_db.get_all_db_files()

    assert error.value.reason == 'Data Base error'
    assert str(error.value.message) == "Some OS Error during get_all_files"


def test_get_file_content_succeed(tmpdir):
    mock_dir = tmpdir.mkdir('test_db')
    mock_dir.join('file1.json').write({1: 1})
    test_db = DB('test_db', tmpdir.strpath)

    content = test_db.get_file_content('file1')

    assert content == '{1: 1}'


@patch('builtins.open')
def test_get_file_content_failed(mock_file_open, tmpdir):
    mock_dir = tmpdir.mkdir('test_db')
    mock_dir.join('file1.json').write({1: 1})
    test_db = DB('test_db', tmpdir.strpath)

    mock_file_open.side_effect = OSError(
        "Some OS Error during get_file_content"
    )

    with pytest.raises(DBErrors) as error:
        test_db.get_file_content('file1')

    assert error.value.reason == 'Data Base error'
    assert str(error.value.message) == "Some OS Error during get_file_content"


def test_create_file_succeed(tmpdir):
    mock_dir = tmpdir.mkdir('test_db')
    file_name = f"test_file-{uuid4()}"
    content = json.dumps({'content': 'test_create_file_succeed'})
    test_db = DB('test_db', tmpdir.strpath)

    test_db.create_file(file_name, content)

    assert mock_dir.join(f'{file_name}.{test_db.db_file_extension}').isfile()
    assert test_db.get_file_content(file_name) == content


@patch('builtins.open')
def test_create_file_failed(mock_file_open, tmpdir):
    mock_file_open.side_effect = OSError(
        "Some OS Error during create_file"
    )

    mock_dir = tmpdir.mkdir('test_db')
    file_name = f"test_file-{uuid4()}"
    content = json.dumps({'content': 'test_create_file_succeed'})
    test_db = DB('test_db', tmpdir.strpath)

    with pytest.raises(DBErrors) as error:
        test_db.create_file(file_name, content)

    assert not mock_dir.join(
        f'{file_name}.{test_db.db_file_extension}'
    ).isfile()
    assert error.value.reason == 'Data Base error'
    assert str(error.value.message) == "Some OS Error during create_file"


def test_update_file_succeed(tmpdir):
    mock_dir = tmpdir.mkdir('test_db')
    file_name = f"test_file-{uuid4()}"
    old_content = json.dumps({'content': 'old_content'})
    test_db = DB('test_db', tmpdir.strpath)
    mock_dir.join(
        f'{file_name}.{test_db.db_file_extension}'
    ).write(old_content)
    new_content = json.dumps({'content': 'new_content'})

    test_db.update_file(file_name, new_content)

    assert mock_dir.join(f'{file_name}.{test_db.db_file_extension}').isfile()
    assert test_db.get_file_content(file_name) == new_content


def test_update_file_failed(tmpdir):
    mock_dir = tmpdir.mkdir('test_db')
    file_name = f"test_file-{uuid4()}"
    old_content = json.dumps({'content': 'old_content'})
    test_db = DB('test_db', tmpdir.strpath)
    mock_dir.join(
        f'{file_name}.{test_db.db_file_extension}'
    ).write(old_content)
    new_content = json.dumps({'content': 'new_content'})

    with patch('builtins.open', side_effect=OSError(
            "Some OS Error during update_file")):
        with patch('service.db.os.path', return_value=True):
            with pytest.raises(DBErrors) as error:
                test_db.update_file(file_name, new_content)

    assert error.value.reason == 'Data Base error'
    assert str(error.value.message) == "Some OS Error during update_file"
    assert mock_dir.join(f'{file_name}.{test_db.db_file_extension}').isfile()
    assert test_db.get_file_content(file_name) == old_content


def test_delete_file_succeed(tmpdir):
    mock_dir = tmpdir.mkdir('test_db')
    mock_dir.join('file1.json').write({1: 1})
    mock_dir.join('file2.json').write({2: 2})
    test_db = DB('test_db', tmpdir.strpath)

    test_db.delete_file('file1')

    assert not mock_dir.join('file1.json').isfile()
    assert mock_dir.join('file2.json').isfile()


@patch('service.db.os')
def test_delete_file_failed(mock_os, tmpdir):
    mock_os.remove.side_effect = OSError('Some OS Error during delete_file')

    mock_dir = tmpdir.mkdir('test_db')
    mock_dir.join('file1.json').write({1: 1})
    mock_dir.join('file2.json').write({2: 2})
    test_db = DB('test_db', tmpdir.strpath)

    with pytest.raises(DBErrors) as error:
        test_db.delete_file('file1')

    assert error.value.reason == 'Data Base error'
    assert str(error.value.message) == "Some OS Error during delete_file"
    assert mock_dir.join('file1.json').isfile()
    assert mock_dir.join('file2.json').isfile()
