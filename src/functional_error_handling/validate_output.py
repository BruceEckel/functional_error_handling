#: validate_output.py
# Validate example output using
# console == """output string"""
# Or
# console == "output string"
# Update scripts using: python validate_output.py *
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
    # init=False means do not include this field in the generated __init__ method
    captured_output: StringIO = field(default_factory=StringIO, init=False)
    # lambda forces evaluation at instance creation, not class creation:
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
        if captured_text != expected_text:
            print(
                f"--Mismatch--\nExpected:\n{expected_text.strip()}\nGot:\n{captured_text}"
            )
        self.captured_output = StringIO()  # Clear buffer for the next capture
        sys.stdout = TeeStream(self.original_stdout, self.captured_output)
        sys.stderr = TeeStream(self.original_stderr, self.captured_output)
        return True


console = OutputValidator()  # Global to use in scripts

# Remainder of file is for updating 'console ==' expressions in scripts.
# Check all python scripts:
# python validate_output.py *
# Check foo.py and bar.py:
# python validate_output.py foo.py bar.py


def capture_script_output(script_path: Path, temp_content: str) -> str:
    "Temporarily rewrite the script for output capture, run it, then restore original"
    original_content = script_path.read_text()
    script_path.write_text(temp_content)  # temp_content does not redirect output

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)], capture_output=True, text=True
        )
        return result.stdout
    finally:  # Always restore original content
        script_path.write_text(original_content)


def update_script_with_output(script_path: Path, outputs: List[str]) -> bool:
    "Update the 'console ==' lines with the new outputs"
    original_script = script_path.read_text()
    modified_script = original_script

    delimiter = "END_OF_CONSOLE_OUTPUT_SECTION"
    pattern = re.compile(r'(console\s*==\s*("""|")([\s\S]*?)\2)')
    matches = list(pattern.finditer(original_script))

    # Replace the console placeholders with delimiter prints in the temp script
    for match in matches:
        placeholder_text = f'print("{delimiter}")'  # Replace each console match
        modified_script = modified_script.replace(match.group(0), placeholder_text)

    # Capture output using the modified script
    output = capture_script_output(script_path, modified_script)
    output_sections = output.split(delimiter)  # Split output by delimiter

    # Update original script with new outputs
    modified_script = original_script
    for match, new_output in zip(matches, output_sections):
        quotes = match.group(2)
        match quotes:
            case '"""':
                new_output_formatted = f'"""\n{new_output.strip()}\n"""'
            case '"':
                new_output_formatted = f'"{new_output.replace("\n", " ").strip()}"'
            case _:
                raise Exception(f"{quotes = } Neither single nor triple quotes")

        modified_script = modified_script.replace(
            match.group(0), f"console == {new_output_formatted}"
        )

    if modified_script != original_script:
        script_path.write_text(modified_script)
        # print("-" * 60)
        # print(modified_script)
        return True  # Indicate that changes were made
    return False  # Indicate no changes were made


def main(file_args: List[str]):
    this_script_name = Path(__file__).name
    console_import_line = "from validate_output import console"
    for file_pattern in file_args:
        for file in Path(".").glob(file_pattern):
            if file.name.endswith(".py") and file.name != this_script_name:
                content = file.read_text()
                if console_import_line in content:
                    print(f"Processing {file}", end=": ")
                    temp_content = content.replace(console_import_line, "console = ''")
                    output = capture_script_output(file, temp_content)
                    outputs = [out.strip() for out in output.split("\n") if out.strip()]
                    if update_script_with_output(file, outputs):
                        print(f"\n\tUpdated {file} with console outputs.")
                    else:
                        print("no changes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update 'console ==' sections of Python scripts"
    )
    parser.add_argument("files", nargs="+", help="File names or patterns to process")
    main(parser.parse_args().files)
