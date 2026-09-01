import json
import pytest

from lib.errors import fail


class TestFail:
    def test_exits_with_code_1(self):
        with pytest.raises(SystemExit) as exc_info:
            fail("something went wrong")
        assert exc_info.value.code == 1

    def test_prints_json_to_stderr(self, capsys):
        with pytest.raises(SystemExit):
            fail("something went wrong")

        captured = capsys.readouterr()
        parsed = json.loads(captured.err)
        assert parsed == {"error": "something went wrong"}

    def test_nothing_on_stdout(self, capsys):
        with pytest.raises(SystemExit):
            fail("oops")

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_message_preserved_verbatim(self, capsys):
        msg = "Unable to locate Graph Engineering framework. Expected file at: '/foo/bar'."
        with pytest.raises(SystemExit):
            fail(msg)

        captured = capsys.readouterr()
        parsed = json.loads(captured.err)
        assert parsed["error"] == msg
