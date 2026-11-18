# Downloads Test Cases

**Automation:** `tests/ui/test_09_downloads.py`  |  **Report:** `reports/downloads/Downloads test <DD-MM-YYYY>_<HH-mm-ss>.html` (all reports: `reports/index.html`)
**Application:** https://testautomationpractice.blogspot.com/  |  **ID prefix:** `TC_DOWNLOAD_`  |  **Master CSV:** `docs/test-cases/downloads.csv`

## Overview
The 'Download Files' page creates a text file or a PDF file from the text typed by the user. The browser downloads the files into a temporary folder that belongs to the test.

## Scope and notes
- Every case has its own browser and its own empty download folder, so parallel runs never see each other's files.
- Site quirk: the "PDF" file only holds the typed text with a .pdf extension; it is not a real PDF document (checked on purpose in TC_DOWNLOAD_02).

## Downloads

| ID | Title | Priority | Type | Preconditions | Test data | Steps | Expected result | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_DOWNLOAD_01 | Generate and download a text file with the text "Hello from Selenium" and check its name and content. | P1 - Critical | Functional | Browser is open on the 'Download Files' page of the practice site; the browser downloads into an empty temporary folder | "Hello from Selenium" | 1. Type the text in the text area.<br>2. Click the button that generates the text file.<br>3. Wait for the download.<br>4. Read the file. | The file "info.txt" is downloaded and holds "Hello from Selenium". | Automated `test_09_downloads.py::TestDownloads::test_tc_download_01_download_text_file` |
| TC_DOWNLOAD_02 | Generate and download a PDF file with the text "PDF content" and check its name and content. | P1 - Critical | Functional | Browser is open on the 'Download Files' page of the practice site; the browser downloads into an empty temporary folder | "PDF content" | 1. Type the text in the text area.<br>2. Click the button that generates the PDF file.<br>3. Wait for the download.<br>4. Read the file bytes. | The file "info.pdf" is downloaded and its bytes are exactly "PDF content" (site quirk: not a real PDF). | Automated `test_09_downloads.py::TestDownloads::test_tc_download_02_download_pdf_file` |
| TC_DOWNLOAD_03 | Generate the text file and check the download link is named "info.txt". | P3 - Medium | UI | Browser is open on the 'Download Files' page of the practice site; the browser downloads into an empty temporary folder | "x" | 1. Type "x" in the text area.<br>2. Click the button that generates the text file.<br>3. Read the download name of the link. | The download name is "info.txt". | Automated `test_09_downloads.py::TestDownloads::test_tc_download_03_download_link_names` |

## Summary

| Group | Cases | Automated |
| --- | --- | --- |
| Downloads | 3 | 3 |
| **Total** | **3** | **3** |
