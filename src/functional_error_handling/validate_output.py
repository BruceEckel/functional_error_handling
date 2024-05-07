#: validate_output.py
# Ensure correctness of example output using
# console == """
# output string
# """
# Update scripts using: python update_output.py *
import atexit
import sys
from io import StringIO


class TeeStream:
    def __init__(self, main_stream, capture_stream):
        self.main_stream = main_stream
        self.capture_stream = capture_stream

    def write(self, data: str):
        self.main_stream.write(data)
        self.capture_stream.write(data)

    def flush(self):
        self.main_stream.flush()
        self.capture_stream.flush()


class OutputValidator:
    def __init__(self):
        self.start()
        atexit.register(self.stop)

    def start(self):
        "Capture and mirror output"
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.captured_output = StringIO()
        sys.stdout = TeeStream(self.original_stdout, self.captured_output)
        sys.stderr = TeeStream(self.original_stderr, self.captured_output)

    def stop(self):
        "Restore original stdout and stderr"
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    def __eq__(self, other: object) -> bool:
        "Compare captured output to expected output"
        # Standard __eq__ requires `other` to be an object:
        assert isinstance(other, str), f"{other} must be str for console =="
        self.stop()
        captured_text = self.captured_output.getvalue().strip()
        expected_text = other.strip()
        assert (
            captured_text == expected_text
        ), f"\nExpected:\n{expected_text}\nGot:\n{captured_text}"
        self.start()
        return True


console = OutputValidator()  # Global to use in scripts
