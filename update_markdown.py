import argparse
from pathlib import Path
import re


def update_markdown_with_source_code(markdown_file: Path) -> None:
    markdown_content = markdown_file.read_text()

    code_location_matches = re.findall(
        r"<!-- #[code_location] (.+?) -->", markdown_content
    )
    for code_location in code_location_matches:
        code_location_path = Path(code_location)
        if code_location_path.exists() and code_location_path.is_dir():
            for code_file in code_location_path.glob("**/*.py"):
                code_content = code_file.read_text()
                markdown_content = markdown_content.replace(
                    f"```python\n#: {code_file.relative_to(code_location_path)}",
                    f"```python\n{code_content}",
                )

    markdown_file.write_text(markdown_content)


def main():
    parser = argparse.ArgumentParser(
        description="Update Python source-code listings in a markdown document"
    )
    parser.add_argument("markdown_file", type=str, help="Path to the markdown file")
    args = parser.parse_args()

    markdown_file_path = Path(args.markdown_file)
    update_markdown_with_source_code(markdown_file_path)


if __name__ == "__main__":
    main()
