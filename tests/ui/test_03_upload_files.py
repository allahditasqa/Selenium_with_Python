"""Upload Files: single and multiple file upload."""

import pytest

from utils.file_utils import create_text_file


@pytest.mark.regression
class TestUpload:
    def test_tc_upload_01_upload_single_file(self, home, tmp_path):
        """TC_UPLOAD_01 - Upload the text file "single.txt" (5 bytes) and check the status shows name, size and type."""
        file = create_text_file(tmp_path, "single.txt", "hello")
        status = home.upload.upload_single(file)
        assert "single.txt" in status
        assert "Size: 5 bytes" in status
        assert "text/plain" in status

    def test_tc_upload_02_upload_multiple_files(self, home, tmp_path):
        """TC_UPLOAD_02 - Upload three text files "file1.txt", "file2.txt" and "file3.txt" together and check all names are listed."""
        files = [create_text_file(tmp_path, f"file{i}.txt", "x" * i) for i in (1, 2, 3)]
        status = home.upload.upload_multiple(files)
        assert status.startswith("Multiple files selected")
        for file in files:
            assert file.name in status

    def test_tc_upload_03_upload_without_selecting_file_shows_message(self, home):
        """TC_UPLOAD_03 - Click Upload Single File without choosing a file and check a message is shown."""
        home.upload.click(home.upload.SINGLE_BUTTON)
        assert home.upload.single_status() != ""
