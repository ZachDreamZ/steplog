import time
import pytest
from steplog import step, output, StepResult
from steplog.core import Spinner, _strip_ansi, _fmt_time


def test_step_success():
    with step("hello") as r:
        time.sleep(0.01)
    assert isinstance(r, StepResult)
    assert r.label == "hello"
    assert r.success is True
    assert r.duration > 0


def test_step_failure(capsys):
    try:
        with step("failing"):
            time.sleep(0.01)
            raise ValueError("boom")
    except ValueError:
        pass
    captured = capsys.readouterr()
    assert "✗" in captured.out or "boom" in captured.out


def test_step_nested():
    with step("outer") as r1:
        with step("inner") as r2:
            time.sleep(0.01)
    assert r1.success is True
    assert r2.success is True
    assert r1.duration > r2.duration


def test_output_info(capsys):
    output.info("test message")
    assert "test message" in capsys.readouterr().out


def test_output_success(capsys):
    output.success("all good")
    assert "all good" in capsys.readouterr().out


def test_output_warn(capsys):
    output.warn("caution")
    assert "caution" in capsys.readouterr().out


def test_output_error(capsys):
    output.error("oops")
    assert "oops" in capsys.readouterr().out


def test_output_header(capsys):
    output.header("Section Title")
    out = capsys.readouterr().out
    assert "Section Title" in out


def test_output_subheader(capsys):
    output.subheader("sub")
    assert "sub" in capsys.readouterr().out


def test_output_section(capsys):
    output.section("Major")
    assert "Major" in capsys.readouterr().out


def test_output_table(capsys):
    output.table(["Name", "Age"], [["Alice", "30"], ["Bob", "25"]])
    out = capsys.readouterr().out
    assert "Alice" in out
    assert "Bob" in out


def test_output_table_empty(capsys):
    output.table(["Name", "Age"], [])
    out = capsys.readouterr().out
    assert out.strip() == ""


def test_output_code(capsys):
    output.code("line1\nline2")
    out = capsys.readouterr().out
    assert "line1" in out
    assert "line2" in out


def test_output_json(capsys):
    output.json({"key": "value", "nested": {"a": 1}})
    out = capsys.readouterr().out
    assert "key" in out
    assert "value" in out


def test_output_divider(capsys):
    output.divider()
    out = capsys.readouterr().out
    assert "─" in out


def test_output_raw(capsys):
    output.raw("plain text")
    assert "plain text" in capsys.readouterr().out


def test_spinner_lifecycle():
    s = Spinner("loading")
    s.start()
    time.sleep(0.05)
    s.stop(True)
    s.stop(False)


def test_spinner_no_start():
    s = Spinner("never started")
    s.stop(True)


def test_step_result_str():
    r1 = StepResult("test", 0.5, True)
    r2 = StepResult("test", 0.5, False, "error msg")
    assert "✓" in str(r1)
    assert "✗" in str(r2)
    assert "error msg" in str(r2)


def test_fmt_time_ms():
    assert _fmt_time(0.5) == "500ms"


def test_fmt_time_sec():
    assert _fmt_time(1.5) == "1.5s"


def test_fmt_time_zero():
    assert _fmt_time(0.001) == "1ms"


def test_strip_ansi():
    plain = _strip_ansi("\033[92mhello\033[0m")
    assert plain == "hello"


def test_strip_ansi_no_ansi():
    plain = _strip_ansi("hello world")
    assert plain == "hello world"


def test_step_result_defaults():
    r = StepResult("test", 0.0, True)
    assert r.message is None


def test_multiple_output_types(capsys):
    output.header("H")
    output.info("I")
    output.success("S")
    output.warn("W")
    output.error("E")
    output.divider()
    out = capsys.readouterr().out
    for char in ["H", "I", "S", "W", "E"]:
        assert char in out


def test_table_variable_widths(capsys):
    output.table(
        ["Short", "Very Long Header"],
        [["a", "b"], ["longer", "c"]],
    )
    out = capsys.readouterr().out
    assert "Very Long Header" in out


def test_json_empty(capsys):
    output.json({})
    out = capsys.readouterr().out
    assert "{}" in out
