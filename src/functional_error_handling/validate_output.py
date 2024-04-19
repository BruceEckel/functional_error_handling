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
