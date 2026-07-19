import time
from steplog import step, output, StepResult


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


def test_output_info(capsys):
    output.info("test message")
    captured = capsys.readouterr()
    assert "test message" in captured.out


def test_output_success(capsys):
    output.success("all good")
    captured = capsys.readouterr()
    assert "all good" in captured.out


def test_output_warn(capsys):
    output.warn("caution")
    captured = capsys.readouterr()
    assert "caution" in captured.out


def test_output_error(capsys):
    output.error("oops")
    captured = capsys.readouterr()
    assert "oops" in captured.out


def test_output_header(capsys):
    output.header("Section Title")
    captured = capsys.readouterr()
    assert "Section Title" in captured.out


def test_output_table(capsys):
    output.table(["Name", "Age"], [["Alice", "30"], ["Bob", "25"]])
    captured = capsys.readouterr()
    assert "Alice" in captured.out
    assert "Bob" in captured.out


def test_output_section(capsys):
    output.section("Major Section")
    captured = capsys.readouterr()
    assert "Major Section" in captured.out


def test_output_code(capsys):
    output.code("line1\nline2")
    captured = capsys.readouterr()
    assert "line1" in captured.out


def test_output_json(capsys):
    output.json({"key": "value"})
    captured = capsys.readouterr()
    assert "key" in captured.out


def test_output_divider(capsys):
    output.divider()
    captured = capsys.readouterr()
    assert "─" in captured.out


def test_output_raw(capsys):
    output.raw("plain text")
    captured = capsys.readouterr()
    assert "plain text" in captured.out


def test_output_subheader(capsys):
    output.subheader("sub")
    captured = capsys.readouterr()
    assert "sub" in captured.out


def test_spinner():
    s = steplog.core.Spinner("loading")
    s.start()
    time.sleep(0.05)
    s.stop(True)


def test_step_result_str():
    r = StepResult("test", 0.5, True)
    r2 = StepResult("test", 0.5, False, "error msg")
    assert "✓" in str(r)
    assert "✗" in str(r2)
    assert "error msg" in str(r2)


import steplog.core
