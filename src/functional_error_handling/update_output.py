#: update_output.py
# Update 'console ==' expressions in scripts.
# Update all python scripts:
# python update_output.py *
# Update foo.py and bar.py:
# python update_output.py foo.py bar.py
from typing import List
import argparse
import subprocess
import re
import sys
from pathlib import Path


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