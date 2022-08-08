from pathlib import Path
from unittest.mock import patch, mock_open

from test_data.write_to_file_example import write_to_file_example


# Demonstrate how to manually mock file open operations


@patch("test_data.write_to_file_example.open", new_callable=mock_open)
def test_write_to_file(m):
    write_to_file_example("hello", Path("write_to_file_test.txt"))
    m.assert_called_once_with(Path("write_to_file_test.txt"), "w")
    handle = m()
    handle.write.assert_called_once_with("hello")


@patch("test_data.write_to_file_example.open")
def test_write_to_file_without_mock_open(m):
    write_to_file_example("hello", Path("write_to_file_test.txt"))
    m.assert_called_once_with(Path("write_to_file_test.txt"), "w")
    handle = m().__enter__()
    handle.write.assert_called_once_with("hello")
