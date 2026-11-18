"""'Download Files' page: files are generated in the browser and downloaded to a per-test folder."""

import pytest

from utils.file_utils import wait_for_download


@pytest.mark.regression
class TestDownloads:
    def test_tc_download_01_download_text_file(self, download_page, download_dir):
        """TC_DOWNLOAD_01 - Generate and download a text file with the text "Hello from Selenium" and check its name and content."""
        download_page.download_text_file("Hello from Selenium")
        file = wait_for_download(download_dir, ".txt")
        assert file.name == "info.txt"
        assert file.read_text(encoding="utf-8").strip() == "Hello from Selenium"

    def test_tc_download_02_download_pdf_file(self, download_page, download_dir):
        """TC_DOWNLOAD_02 - Generate and download a PDF file with the text "PDF content" and check its name and content."""
        download_page.download_pdf_file("PDF content")
        file = wait_for_download(download_dir, ".pdf")
        assert file.name == "info.pdf"
        # Site quirk: the "PDF" is the typed text saved with a .pdf extension, not a real PDF document.
        assert file.read_bytes() == b"PDF content"

    def test_tc_download_03_download_link_names(self, download_page):
        """TC_DOWNLOAD_03 - Generate the text file and check the download link is named "info.txt"."""
        download_page.type(download_page.TEXT_AREA, "x")
        download_page.click(download_page.GENERATE_TXT)
        assert download_page.txt_download_name() == "info.txt"
