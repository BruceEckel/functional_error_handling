#: all_test.py
# Works with
# rye test
# or
# python -m pytest
# or
# python all_test.py
import os
import subprocess
import sys
from pathlib import Path


def run_script(file_name, throws_exception=False):
    "Run a Python script using subprocess and assert it exits sucessfully"
    script_path = Path(__file__).parent / file_name
    env = os.environ.copy()
    # env["PYTHONPATH"] = str(
    #     Path(__file__).parent
    # )  # Ensure local modules can be imported
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        env=env,
    )
    if throws_exception:
        assert (
            result.returncode != 0
        ), f"Script {file_name} failed with output:\n{result.stdout}\n{result.stderr}"
    else:
        assert (
            result.returncode == 0
        ), f"Script {file_name} failed with output:\n{result.stdout}\n{result.stderr}"
    print(f"{file_name} completed")


def test_example1():
    run_script("example1.py", throws_exception=True)


def test_example2():
    run_script("example2.py")


def test_example3():
    run_script("example3.py")


def test_example4():
    run_script("example4.py")


def test_example5():
    run_script("example5.py")


def test_example6():
    run_script("example6.py")


if __name__ == "__main__":
    test_example1()
    test_example2()
    test_example3()
    test_example4()
    test_example5()
    test_example6()
