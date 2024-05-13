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


def test_comprehension1():
    run_script("comprehension1.py", throws_exception=True)


def test_comprehension2():
    run_script("comprehension2.py")


def test_comprehension3():
    run_script("comprehension3.py")


def test_comprehension4():
    run_script("comprehension4.py")


def test_comprehension5():
    run_script("comprehension5.py")


def test_multiple_arguments():
    run_script("multiple_arguments.py")


if __name__ == "__main__":
    test_comprehension1()
    test_comprehension2()
    test_comprehension3()
    test_comprehension4()
    test_comprehension5()
    test_multiple_arguments()
