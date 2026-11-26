from web import SortwiseApplication


def test_browser_rejects_files_outside_folder(tmp_path):
    app = SortwiseApplication(tmp_path)
    for names in (["../outside.txt"], [str(tmp_path / "file.txt")], []):
        assert "error" in app.execute("sort", {"names": names})


def test_browser_moves_selected_file_and_reports_result(tmp_path, monkeypatch):
    import logger
    import sorter

    (tmp_path / "first.txt").write_text("sort me")
    (tmp_path / "second.txt").write_text("leave me")
    monkeypatch.setattr(logger, "log_file", tmp_path / "log.csv")
    monkeypatch.setattr(sorter, "wait_until_ready", lambda path: True)
    monkeypatch.setattr(sorter, "watch_folder", tmp_path)
    app = SortwiseApplication(tmp_path)
    assert app.execute("scan", {})["total"] == 2
    result = app.execute("sort", {"names": ["first.txt"]})
