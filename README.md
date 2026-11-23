# Sortwise

Sortwise watches a folder and moves completed downloads into categories. It uses CLIP for JPEG and PNG images, a text classifier for PDFs with extractable text, and extension rules for other files. You can review decisions and correct them yourself.

## Setup

Use Python with working PyTorch and Transformers builds. On Windows, use a folder on NTFS. The source and destination must be on the same volume and support hard links. The first image or PDF classification needs internet access to download the model weights unless they are already cached.

Run these commands from the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

By default Sortwise watches your home folder's `Downloads` directory. To try it safely, create a scratch folder and set `watch_folder` in [src/config.py](src/config.py) to that folder. Use copies of a few files.

## Watch, audit and correct

```powershell
.\.venv\Scripts\python.exe src/main.py
```

With the watcher running, copy a test `.txt` file into the watched folder. Once its size stabilizes, it should land in `misc`. Check `sort_log.csv` in the directory where you ran the command. Press Ctrl+C to stop. To process files already present, run `src/bulk_sort.py` instead.

```powershell
.\.venv\Scripts\python.exe src/audit.py "$HOME\Downloads\receipts"
.\.venv\Scripts\python.exe src/correct.py "receipts/report.pdf" documents
```

The audit reports suggested moves. The correction command moves one file and logs it. Use `folder/filename` when a basename is shared by several folders. The path in the audit example assumes the default watch folder.

## How sorting works

The watcher queues new files and browser rename events. It skips common temporary extensions and requires three size readings in a row to match before sorting. A slow download can pause long enough to pass that check, and a file that never settles within the timeout is left for review. Classification errors are reported per file. Sortwise reserves a destination with a hard link before removing the original name, so a duplicate filename gets a numbered suffix.

PDF classification uses extracted text. Image-only PDFs do not get OCR. The optional `src/train.py` experiment fits a classifier from usable image corrections, with at least five examples across two classes. The watcher still uses the default models.

## Working proof

The safety suite passed **4 tests** for download readiness, duplicate filenames, exact correction paths and overwrite prevention. A scratch-file smoke check also moved `example.txt` into `misc` and verified the row in `sort_log.csv`. These checks exercise file handling without loading CLIP or the PDF model. The walkthrough above checks the watcher with your own files.

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m pytest -q tests/test_sorter_safety.py
```

## Browser workspace

Run `python src/web.py` and open [Sortwise](http://sortwise.localhost:8012).
Use `--folder "C:\\path\\to\\scratch"` to choose a scratch directory, or set
`SORTWISE_FOLDER` before starting either entry point. Refresh the file list,
select files, then approve sorting. Activity shows the outcome for each file.
The CSV log is stored in the repository root regardless of the launch folder.

See [architecture and development](docs/ARCHITECTURE.md).
