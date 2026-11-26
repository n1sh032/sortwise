from pathlib import Path

import sorter


def test_wait_until_ready_waits_for_repeated_stable_sizes(tmp_path, monkeypatch):
    path = tmp_path / "download.bin"
    path.write_bytes(b"a")
    sizes = iter([1, 2, 2, 2, 2])
    monkeypatch.setattr(sorter.Path, "stat", lambda self: type("Stat", (), {"st_size": next(sizes)})())
    monkeypatch.setattr(sorter.time, "sleep", lambda _: None)

    assert sorter.wait_until_ready(path, stable_checks=2) is True


def test_unique_destination_does_not_overwrite_existing_file(tmp_path):
    original = tmp_path / "report.pdf"
    original.touch()
    (tmp_path / "report (1).pdf").touch()

    assert sorter.unique_destination(original).name == "report (2).pdf"


def test_find_file_reports_duplicate_names(tmp_path, monkeypatch, capsys):
    import correct

    (tmp_path / "receipts").mkdir()
