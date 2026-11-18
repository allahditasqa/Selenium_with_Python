"""Upload Files: single and multiple file upload."""

import pytest

from utils.file_utils import create_text_file


@pytest.mark.regression
class TestUpload:
    def test_upload_single_file(self, home, tmp_path):
        file = create_text_file(tmp_path, "single.txt", "hello")
        status = home.upload.upload_single(file)
        assert "single.txt" in status
        assert "Size: 5 bytes" in status
        assert "text/plain" in status

    def test_upload_multiple_files(self, home, tmp_path):
        files = [create_text_file(tmp_path, f"file{i}.txt", "x" * i) for i in (1, 2, 3)]
        status = home.upload.upload_multiple(files)
        assert status.startswith("Multiple files selected")
        for file in files:
            assert file.name in status

    def test_upload_without_selecting_file_shows_message(self, home):
        home.upload.click(home.upload.SINGLE_BUTTON)
        assert home.upload.single_status() != ""
