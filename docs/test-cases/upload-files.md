# Upload Files Test Cases

**Automation:** `tests/ui/test_03_upload_files.py`  |  **Report:** `reports/upload-files/Upload Files test <DD-MM-YYYY>_<HH-mm-ss>.html` (all reports: `reports/index.html`)
**Application:** https://testautomationpractice.blogspot.com/  |  **ID prefix:** `TC_UPLOAD_`  |  **Master CSV:** `docs/test-cases/upload-files.csv`

## Overview
The Upload Files section has a single file upload and a multiple file upload, each with a Submit button and a status message.

## Scope and notes
- Small text files are created in a temporary folder by the test; nothing is stored on the site.
- Only the status text is checked; the site does not keep the files.

## Upload

| ID | Title | Priority | Type | Preconditions | Test data | Steps | Expected result | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC_UPLOAD_01 | Upload the text file "single.txt" (5 bytes) and check the status shows name, size and type. | P1 - Critical | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | single.txt, content "hello" | 1. Create the file single.txt with the text hello.<br>2. Choose the file in the single upload input.<br>3. Click Upload Single File.<br>4. Read the status message. | The status contains "single.txt", "Size: 5 bytes" and "text/plain". | Automated `test_03_upload_files.py::TestUpload::test_tc_upload_01_upload_single_file` |
| TC_UPLOAD_02 | Upload three text files "file1.txt", "file2.txt" and "file3.txt" together and check all names are listed. | P1 - Critical | Functional | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | file1.txt (1 byte), file2.txt (2 bytes), file3.txt (3 bytes) | 1. Create the three files.<br>2. Choose all three files in the multiple upload input.<br>3. Click Upload Multiple Files.<br>4. Read the status message. | The status starts with "Multiple files selected" and contains the three file names. | Automated `test_03_upload_files.py::TestUpload::test_tc_upload_02_upload_multiple_files` |
| TC_UPLOAD_03 | Click Upload Single File without choosing a file and check a message is shown. | P2 - High | Negative | Browser is open on the practice site home page (https://testautomationpractice.blogspot.com/) | No file | 1. Do not choose any file.<br>2. Click Upload Single File.<br>3. Read the status message. | A status message is shown (it is not empty). | Automated `test_03_upload_files.py::TestUpload::test_tc_upload_03_upload_without_selecting_file_shows_message` |

## Summary

| Group | Cases | Automated |
| --- | --- | --- |
| Upload | 3 | 3 |
| **Total** | **3** | **3** |
