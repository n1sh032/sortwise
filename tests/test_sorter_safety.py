from pathlib import Path

import sorter


def test_wait_until_ready_waits_for_repeated_stable_sizes(tmp_path, monkeypatch):
    path = tmp_path / "download.bin"
    path.write_bytes(b"a")
    sizes = iter([1, 2, 2, 2, 2])
    monkeypatch.setattr(sorter.Path, "stat", lambda self: type("Stat", (), {"st_size": next(sizes)})())
    monkeypatch.setattr(sorter.time, "sleep", lambda _: None)

