from web import SortwiseApplication


def test_browser_rejects_files_outside_folder(tmp_path):
    app = SortwiseApplication(tmp_path)
    for names in (["../outside.txt"], [str(tmp_path / "file.txt")], []):
        assert "error" in app.execute("sort", {"names": names})


