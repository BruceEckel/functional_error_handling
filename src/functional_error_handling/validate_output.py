#: validate_output.py
# Validate example output using 'console == "output string"'
import sys
import atexit
from io import StringIO
from typing import List, TextIO
from dataclasses import dataclass, field
import argparse
import subprocess
import re
from pathlib import Path


@dataclass(frozen=True)
class TeeStream:
    "Writes to two streams"
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
        "Start capturing and mirroring output"
        sys.stdout = TeeStream(self.original_stdout, self.captured_output)
        sys.stderr = TeeStream(self.original_stderr, self.captured_output)

    def stop(self):
        "Restore original stdout and stderr, stop capturing"
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    def __eq__(self, other: str) -> bool:  # type: ignore
        "Compare captured output to expected output"
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

# Remainder of file is for updating 'console ==' expressions


def capture_script_output(script_path: Path, temp_content: str) -> str:
    "Temporarily rewrite the script for output capture, run it, then restore original"
    original_content = script_path.read_text()
    script_path.write_text(
        temp_content
    )  # Write temporary content that does not redirect output

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)], capture_output=True, text=True
        )
        return result.stdout
    finally:
        script_path.write_text(
            original_content
        )  # Restore original content no matter what happens


def update_script_with_output(script_path, outputs) -> bool:
    "Read script, find 'console ==' and update outputs"
    original_content = script_path.read_text()

    # Regex to handle both triple-double-quoted and single-double-quoted strings
    pattern = re.compile(r'console\s*==\s*(?:"""[\s\S]*?"""|"[^"]*")')

    def replace_with_output(match):
        current_output = outputs.pop(0) if outputs else ""
        quote_type = '"""' if '"""' in match.group(0) else '"'
        return f"console == {quote_type}\n{current_output.strip()}\n{quote_type}"

    new_content = pattern.sub(replace_with_output, original_content)

    # Write back to the file only if changes have occurred
    if new_content != original_content:
        script_path.write_text(new_content)
        return True  # Changed
    return False  # Unchanged


def main(file_args: List[str]):
    this_script_name = Path(__file__).name
    console_import_line = "from validate_output import console"
    for file_pattern in file_args:
        for file in Path(".").glob(file_pattern):
            if file.name.endswith(".py") and file.name != this_script_name:
                content = file.read_text()
                if console_import_line in content:
                    print(f"Processing {file}", end=" ... ")
                    temp_content = content.replace(console_import_line, "console = ''")
                    output = capture_script_output(file, temp_content)
                    print(f"\n{output = }\n")
                    outputs = re.split(r'console\s*==\s*"""|"""', output)[1::2]
                    if update_script_with_output(file, outputs):
                        print(f"Updated {file} with console outputs.")
                    else:
                        print(f"No changes made to {file}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update 'console ==' sections of Python scripts"
    )
    parser.add_argument("files", nargs="+", help="File names or patterns to process")
    main(parser.parse_args().files)


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
