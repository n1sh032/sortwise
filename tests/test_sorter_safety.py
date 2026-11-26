from pathlib import Path

import sorter
import pytest
from file_move import move_without_overwrite


def test_move_does_not_replace_existing_destination(tmp_path):
    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"
    source.write_text("source")
    destination.write_text("destination")
    with pytest.raises(FileExistsError):
        move_without_overwrite(source, destination)
    assert source.read_text() == "source"
    assert destination.read_text() == "destination"

    destination.unlink()


def test_wait_until_ready_waits_for_repeated_stable_sizes(tmp_path, monkeypatch):
    path = tmp_path / "download.bin"
    path.write_bytes(b"a")
    sizes = iter([1, 2, 2, 2, 2])
    class Download:
        def stat(self):
            return type("Stat", (), {"st_size": next(sizes)})()
    monkeypatch.setattr(sorter.time, "sleep", lambda _: None)

    assert sorter.wait_until_ready(Download(), stable_checks=2) is True


def test_unique_destination_does_not_overwrite_existing_file(tmp_path):
    original = tmp_path / "report.pdf"
    original.touch()
    (tmp_path / "report (1).pdf").touch()

    assert sorter.unique_destination(original).name == "report (2).pdf"


def test_find_file_reports_duplicate_names(tmp_path, monkeypatch, capsys):
    import correct

    (tmp_path / "receipts").mkdir()
    (tmp_path / "documents").mkdir()
    (tmp_path / "receipts" / "same.pdf").touch()
    (tmp_path / "documents" / "same.pdf").touch()
    monkeypatch.setattr(correct, "watch_folder", tmp_path)

    assert correct.find_file("same.pdf") is None
    assert str(Path("receipts") / "same.pdf") in capsys.readouterr().out
    assert correct.find_file("receipts/same.pdf") == tmp_path / "receipts" / "same.pdf"
