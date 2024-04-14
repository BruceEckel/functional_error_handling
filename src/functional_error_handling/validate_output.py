#: validate_output.py
# Validate example output using 'console == "ouput string"'
import sys
import atexit
from io import StringIO
from typing import Optional, TextIO
from dataclasses import dataclass, field


class TeeStream:
    "Writes to two streams."

    def __init__(self, main_stream: TextIO, capture_stream: StringIO):
        self.main_stream = main_stream
        self.capture_stream = capture_stream

    def write(self, data):
        self.main_stream.write(data)
        self.capture_stream.write(data)

    def flush(self):
        self.main_stream.flush()
        self.capture_stream.flush()


@dataclass
class OutputValidator:
    captured_output: StringIO = field(default_factory=StringIO, init=False)
    original_stdout: Optional[TextIO] = field(default=None, init=False)
    original_stderr: Optional[TextIO] = field(default=None, init=False)

    def __post_init__(self):
        self.start()
        atexit.register(self.stop)  # Ensure cleanup on exit

    def start(self):
        "Start capturing and mirroring output."
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
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
        self.captured_output = StringIO()  # Clear the buffer for the next capture
        sys.stdout = TeeStream(self.original_stdout, self.captured_output)
        sys.stderr = TeeStream(self.original_stderr, self.captured_output)
        if captured_text != expected_text:
            print(f"! Expected:\n{expected_text}\n! Got:\n{captured_text}")
        return True


# Create a global instance to use in scripts
console = OutputValidator()
