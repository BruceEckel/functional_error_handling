#: all_test.py
# Works with pytest or as a standalone test
import subprocess
from pathlib import Path


def run_script(file_name, throws_exception=False):
    "Run a Python script using subprocess and assert it exits OK"
    script_path = Path(__file__).parent / file_name
    result = subprocess.run(
        ["python", str(script_path)], capture_output=True, text=True
    )
    if throws_exception:
        assert (
            result.returncode != 0
        ), f"Script {file_name} failed with output:\n{result.stdout}\n{result.stderr}"
    else:
        assert (
            result.returncode == 0
        ), f"Script {file_name} failed with output:\n{result.stdout}\n{result.stderr}"


def test_comprehension1():
    run_script("comprehension1.py", throws_exception=True)


def test_comprehension2():
    run_script("comprehension2.py")


def test_comprehension3():
    run_script("comprehension3.py")


def test_composed():
    run_script("composed.py")


def test_do_notation():
    run_script("do_notation.py")
