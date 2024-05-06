import argparse
import re
import sys
from typing import List
from dataclasses import dataclass
from pathlib import Path
from pprint import pformat


@dataclass
class Listing:
    filename: str
    content: str
    source_file: Path

    def __str__(self):
        return f"""
Filename from slugline: {self.filename}
Source File: {self.source_file.absolute() if self.source_file else ""}
Markdown Content:
{self.content}
{'-' * 60}
"""
        # Source File: {self.source_file.name if self.source_file else ""}


def find_python_files_and_listings(markdown_content: str) -> List[Listing]:
    """
    Find all #[code_location] paths in the markdown content and
    return associated Python files and listings.
    """
    listings = []
    python_files = []

    code_location_pattern = re.compile(r"#\[code_location\]\s*(.*)\s*-->")

    for match in re.finditer(code_location_pattern, markdown_content):
        code_location = match.group(1)
        print(f"{code_location = }")
        path = Path(code_location)
        if path.is_absolute():
            python_files.extend(list(path.glob("**/*.py")))
        else:
            python_files.extend(list((Path.cwd() / path).resolve().glob("**/*.py")))
    available_python_files = [p.name for p in python_files]
    print(f"python_files = {pformat(available_python_files)}")

    # If slug line doesn't exist group(1) returns None:
    listing_pattern = re.compile(r"```python\n(#\:(.*?)\n)?(.*?)```", re.DOTALL)
    for match in re.finditer(listing_pattern, markdown_content):
        listing_content = (match.group(1) or "") + match.group(3)
        filename = match.group(2).strip() if match.group(2) else None
        assert filename, f"filename not found in {match}"
        # print(f"{filename = }")
        source_file = next(
            (file for file in python_files if file.name == filename), None
        )
        if not source_file:
            print(f"{filename = } not found in {pformat(available_python_files)}")
            sys.exit(1)
        listings.append(Listing(filename, listing_content, source_file))
    return listings


def update_markdown_content(
    markdown_content: str, listings: List[Listing], updated_content: List[str]
) -> str:
    """Update the markdown content with the updated content."""
    updated_markdown_content = markdown_content
    for index, listing in enumerate(listings):
        updated_markdown_content = re.sub(
            r"```python(.*?)```",
            f"```python\n{updated_content[index]}```",
            updated_markdown_content,
            count=1,
            flags=re.DOTALL,
        )
    return updated_markdown_content


def main():
    parser = argparse.ArgumentParser(
        description="Update Python source-code listings within a markdown file."
    )
    parser.add_argument(
        "markdown_file", help="Path to the markdown file to be updated."
    )
    args = parser.parse_args()

    markdown_file_path = args.markdown_file
    markdown_file = Path(markdown_file_path)
    markdown_content = markdown_file.read_text(encoding="utf-8")
    listings = find_python_files_and_listings(markdown_content)
    for listing in listings:
        print(listing)
    sys.exit(0)

    updated_content = []
    for listing in listings:
        if listing.source_file:
            with open(listing.source_file, "r") as file:
                python_content = file.read()
            if python_content != listing.content:
                updated_content.append(python_content)
            else:
                updated_content.append(listing.content)
        else:
            updated_content.append(listing.content)

    updated_markdown_content = update_markdown_content(
        markdown_content, listings, updated_content
    )
    markdown_file.write_text(updated_markdown_content, encoding="utf-8")
    print("Markdown file updated successfully!")


if __name__ == "__main__":
    main()
