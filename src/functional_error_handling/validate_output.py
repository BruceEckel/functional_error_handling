#: validate_output.py
# Validate example output using 'console == "ouput string"'
import sys
import atexit
from io import StringIO
from typing import TextIO
from dataclasses import dataclass, field
import argparse
import subprocess
import re
from pathlib import Path


@dataclass(frozen=True)
class TeeStream:
    "Writes to two streams."
    main_stream: TextIO
    capture_stream: StringIO

    def write(self, data: str) -> None:
        self.main_stream.write(data)
        self.capture_stream.write(data)

    def flush(self) -> None:
        self.main_stream.flush()
        self.capture_stream.flush()


@dataclass
class OutputValidator:
    captured_output: StringIO = field(default_factory=StringIO, init=False)
    original_stdout: TextIO = field(default_factory=lambda: sys.stdout, init=False)
    original_stderr: TextIO = field(default_factory=lambda: sys.stderr, init=False)

    def __post_init__(self):
        self.start()
        atexit.register(self.stop)  # Ensure cleanup on exit

    def start(self):
        "Start capturing and mirroring output."
        sys.stdout = TeeStream(self.original_stdout, self.captured_output)
        sys.stderr = TeeStream(self.original_stderr, self.captured_output)

    def stop(self):
        "Restore original stdout and stderr, stop capturing."
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    def __eq__(self, other: str) -> bool:  # type: ignore
        "Compare captured output to expected output."
        sys.stdout.flush()
        sys.stderr.flush()
        captured_text = self.captured_output.getvalue().strip()
        expected_text = other.strip()
        assert (
            captured_text == expected_text
        ), f"Expected:\n{expected_text.strip()}\nGot:\n{captured_text}"
        self.captured_output = StringIO()  # Clear buffer for the next capture
        sys.stdout = TeeStream(self.original_stdout, self.captured_output)
        sys.stderr = TeeStream(self.original_stderr, self.captured_output)
        return True


console = OutputValidator()  # Global to use in scripts


def capture_script_output(script_path: Path) -> SyntaxWarning:
    "Execute a script and capture its output"
    result = subprocess.run(
        [sys.executable, str(script_path)], capture_output=True, text=True
    )
    return result.stdout


def update_script_with_output(script_path: Path, outputs) -> None:
    "Read the script, find 'console ==' and update the outputs"
    content = Path(script_path).read_text()
    pattern = re.compile(r'(console\s*==\s*"""[\s\S]*?""")')

    def replace_with_output(match):
        current_output = outputs.pop(0) if outputs else ""
        return f'console == """\n{current_output.strip()}\n"""'

    new_content = pattern.sub(replace_with_output, content)
    Path(script_path).write_text(new_content)


def main(files):
    for file_pattern in files:
        script_path = Path(file_pattern)
        print(f"Processing {script_path}...")
        output = capture_script_output(script_path)
        outputs = output.split('console == """')[
            1:
        ]  # Split the output based on our delimiter
        outputs = [
            out.split('"""')[0] for out in outputs
        ]  # Extract the actual outputs between the delimiters
        update_script_with_output(script_path, outputs)
        print(f"Updated {script_path} 'console ==' outputs.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update 'console ==' sections of Python scripts"
    )
    parser.add_argument("files", nargs="+", help="File names or patterns to process.")
    args = parser.parse_args()
    main(args.files)


""" Notes:
If you directly assign sys.stdout or sys.stderr as defaults, like
original_stdout: TextIO = sys.stdout
the value is evaluated at the time the class is defined, not when
instances are created. This means every instance would use the
same sys.stdout and sys.stderr that were present when the class
was first loaded, ignoring any changes made to these streams between
the class definition and instance creation. By using lambda: sys.stdout,
the function is executed each time an instance is initialized, thereby
always capturing the current sys.stdout and sys.stderr at that moment.
This is more flexible and accurate in environments where the standard
streams might be redirected or modified.


In a Python dataclass, the init=False parameter within a field
specification indicates that the field should not be included
as a parameter in the automatically generated __init__ method
of the dataclass. This means that the field will not be initialized
via the constructor of the class, but rather it should be set or
initialized internally within the class, typically in methods
like __post_init__ or directly within the body of the class.
"""
