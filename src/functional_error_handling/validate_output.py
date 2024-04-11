#: validate_output.py
# Validates string output blocks tagged with '='
import sys
from pathlib import Path
from io import StringIO
import textwrap


class CaptureOutput:
    def __init__(self):
        # Save reference to original standard output:
        self.original_stdout = sys.stdout

    def __enter__(self):
        self.captured_output = StringIO()
        # Redirect standard output to StringIO:
        sys.stdout = self.captured_output
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Reset standard output:
        sys.stdout = self.original_stdout

    def get(self) -> str:
        return self.captured_output.getvalue().strip()

    def flush(self):
        self.captured_output = StringIO()
        sys.stdout = self.captured_output


def compare_output_with_expected(code: str):
    parts = code.split('"""=')
    code_executable = parts[0]
    expected_outputs = parts[1:]

    # Execute the initial block of code
    with CaptureOutput() as capture:
        print(f"{code_executable = }")
        exec(code_executable, globals())

    # Iterate over expected outputs and compare
    for expected in expected_outputs:
        expected = expected.strip()
        actual = capture.get().strip()
        if actual != expected:
            print(
                textwrap.dedent(
                    f"""Mismatch:
                    {expected = }
                    {actual}
                    """
                )
            )
        capture.flush()  # Prepare for the next iteration


def validate():
    # Read the current file and check it
    # Determine the current file path
    current_file_path = Path(__file__)
    print(f"checking {current_file_path = }")
    # Read the content of the current file
    code = current_file_path.read_text()
    # Perform output comparison
    compare_output_with_expected(code)
