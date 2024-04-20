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

console_import_line = "from validate_output import console"
output_section_delimiter = "END_OF_CONSOLE_OUTPUT_SECTION"

__trace = True
__trace = False


def trace(msg: str):
    if __trace:
        print(msg)


def capture_script_output(script_path: Path, temp_content: str) -> str:
    "Temporarily rewrite the script for output capture, run it, then restore original"
    original_content = script_path.read_text()
    script_path.write_text(temp_content)  # temp_content does not redirect output

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)], capture_output=True, text=True
        )
        # Check if the script ran successfully
        if result.returncode != 0:
            print(temp_content)
            print("--- Temporary script did not run successfully ---")
            sys.exit(result.returncode)
        return result.stdout
    finally:  # Always restore original content
        script_path.write_text(original_content)


def update_script_with_output(script_path: Path, outputs: List[str]) -> bool:
    "Update 'console ==' lines with the new outputs"
    original_script = script_path.read_text()
    modified_script = original_script
    pattern = re.compile(r'(console\s*==\s*(""")([\s\S]*?)("""))')
    matches = list(pattern.finditer(original_script))
    if __trace:
        for match in matches:
            trace(f"{match.group(0) = }")
            trace(f"{match.group(2) = }")

    # Replace the console placeholders with delimiter prints in the temp script
    for match in matches:
        trace(f"{match.group(0) = }")
        trace(f'print("{output_section_delimiter}")')
        modified_script = modified_script.replace(
            match.group(0), f'print("{output_section_delimiter}")', 1
        )
    trace("modified_script:")
    trace(modified_script)
    if __trace:
        modified_script_path = script_path.with_name(script_path.stem + "_modified.py")
        print(f"{modified_script_path = }")
        modified_script_path.write_text(modified_script)

    # Capture output using the modified script
    output = capture_script_output(script_path, modified_script)
    trace("-" * 60)
    trace("output:")
    trace(output)
    trace("=" * 60)
    output_sections = output.split(output_section_delimiter)
    if __trace:
        for output_section in output_sections:
            trace(f"{output_section = }")

    # Update original script with new outputs
    modified_script = original_script
    for match, new_output in zip(matches, output_sections):
        trace(f"{match.group(0) = }\n\t{new_output = }")
        # match quotes:
        #     case '"""':
        #         new_output_formatted = f'"""\n{new_output.strip()}\n"""'
        #     case '"':
        #         new_output_formatted = f'"{new_output.replace("\n", " ").strip()}"'
        #     case _:
        #         raise ValueError(f"quotes[{quotes}] Neither single nor triple quotes")
        # new_output_formatted = f'"""\n{new_output.strip()}\n"""'
        # trace(f"\t{new_output_formatted = }")
        modified_script = modified_script.replace(
            match.group(0), f'console == """\n{new_output.strip()}\n"""', 1
        )

    trace("-" * 20 + " modified_script: " + "-" * 20)
    trace(modified_script)

    if modified_script != original_script:
        if __trace:
            script_path = script_path.with_name(script_path.stem + "_temp.py")
            print("-" * 20 + f" {script_path} " + "-" * 20)
            print(modified_script)
        script_path.write_text(modified_script)
        return True  # Changes made
    return False  # No changes made


def main(file_args: List[str]):
    this_script_name = Path(__file__).name
    for file_pattern in file_args:
        for file in Path(".").glob(file_pattern):
            if file.name.endswith(".py") and file.name != this_script_name:
                content = file.read_text()
                if console_import_line in content:
                    print(f"Processing {file}")
                    temp_content = content.replace(console_import_line, "console = ''")
                    output = capture_script_output(file, temp_content)
                    outputs = [out.strip() for out in output.split("\n") if out.strip()]
                    if update_script_with_output(file, outputs):
                        print(f"\t--> Updated {file} with console outputs.")
                    else:
                        print(f"(No changes to {file})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update 'console ==' output sections in Python scripts"
    )
    parser.add_argument("files", nargs="+", help="File names or patterns to process")
    main(parser.parse_args().files)
