# sortwise

my downloads folder is always a mess so i'm building a script that watches it
and auto-sorts files. also using this as a way to actually learn ML instead
of just watching tutorials without building anything.

## how it works right now

- watches the downloads folder in real time and sorts new files as they come in
- images get classified by CLIP (screenshot / meme / receipt / photo / etc)
  instead of just going by file extension
- pdfs get their text read and classified too (receipt / resume / manual / etc)
- everything else falls back to simple extension based rules, with a "misc"
  folder for anything not covered
- every sort decision gets logged to sort_log.csv
- if the model gets something wrong, correct.py lets you fix it and logs
  the correction as training data
- train.py trains a small classifier on those corrections once there's
  enough of them (still collecting data on this)

## files

- `config.py` - settings, which folder to watch, the extension rules
- `sorter.py` - the actual sorting logic, handles new files as they appear
- `classifier.py` - CLIP setup and image classification
- `doc_classifier.py` - pdf text extraction and classification
- `logger.py` - writes every decision to sort_log.csv
- `correct.py` - manually fix a wrong sort and log it as a correction
- `train.py` - trains a classifier on logged corrections
- `bulk_sort.py` - one time script to sort files already sitting in downloads
- `audit.py` - checks already-sorted files against what the model thinks
  they should be, doesn't move anything automatically

## what i tried and removed

originally had a version that auto-detected corrections by watching for
files being manually dragged between sorted folders. scrapped it because
it couldn't tell the difference between an actual correction and just
reorganizing files for some unrelated reason, so it was logging bad data.
manual correct.py is slower but way more reliable.

## how to run it

pip install -r requirements.txt
python src/main.py


drop a file into your downloads folder while it's running and it should
sort itself.

to sort everything already sitting in downloads:

python src/bulk_sort.py


## why

wanted a project where the ML part is actually doing something useful, not
just a jupyter notebook that ends after the accuracy score. learned watchdog,
zero-shot classification with CLIP, and how to structure a project that
actually improves itself over time instead of being static.