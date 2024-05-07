#: update_markdown_code_listings.py
import argparse
import re
import sys
from typing import List
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pformat
from rich.console import Console

console = Console()
python_files = []


@dataclass
class MarkdownListing:
    slugname: str
    markdown_listing: str
    source_file_path: Path | None
    # Exclude field from constructor arguments:
    source_file_contents: str = field(init=False)
    unchanged: bool = field(init=False)

    def __post_init__(self):
        if self.source_file_path is None:
            console.print(
                "[bold red] MarkdownListing: source_file_path not found among:[/bold red]"
            )
            console.print(pformat(python_files))
            raise ValueError("source_file cannot be None")
        self.source_file_contents = self.source_file_path.read_text(encoding="utf-8")
        self.unchanged = self.markdown_listing == self.source_file_contents

    def __str__(self):
        return f"""
Filename from slugline: {self.slugname}
Source File: {self.source_file_path.absolute() if self.source_file_path else ""}
{self.unchanged = }
Markdown Code Listing:
{self.markdown_listing}
{'-' * 60}
Source File Code Listing:
{self.source_file_contents}
{'=' * 60}
"""


def find_python_files_and_listings(markdown_content: str) -> List[MarkdownListing]:
    """
    Find all #[code_location] paths in the markdown content and
    return associated Python files and listings.
    """
    global python_files
    listings = []

    code_location_pattern = re.compile(r"#\[code_location\]\s*(.*)\s*-->")

    for match in re.finditer(code_location_pattern, markdown_content):
        code_location = Path(match.group(1))
        if code_location.is_absolute():
            python_files.extend(list(code_location.glob("**/*.py")))
        else:  # Relative path:
            python_files.extend(
                list((Path.cwd() / code_location).resolve().glob("**/*.py"))
            )
    console.print(f"python_files = {pformat([p.name for p in python_files])}\n")

    # If slug line doesn't exist group(1) returns None:
    listing_pattern = re.compile(r"```python\n(#\:(.*?)\n)?(.*?)```", re.DOTALL)
    for match in re.finditer(listing_pattern, markdown_content):
        listing_content = (match.group(1) or "") + match.group(3)
        filename = match.group(2).strip() if match.group(2) else None
        assert filename, f"filename not found in {match}"
        source_file = next(
            (file for file in python_files if file.name == filename), None
        )
        listings.append(MarkdownListing(filename, listing_content, source_file))
    return listings


def update_markdown_listings(
    markdown_content: str, listings: List[MarkdownListing]
) -> str:
    for listing in listings:
        if listing.unchanged:
            console.print(f"[bold green]{listing.slugname}")
        if not listing.unchanged:
            console.print(f"[bold red]{listing.slugname}")
            # Perform update:
            # ...


def update_markdown_content(
    markdown_content: str, listings: List[MarkdownListing], updated_content: List[str]
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

    markdown_file = Path(args.markdown_file)
    markdown_content = markdown_file.read_text(encoding="utf-8")
    listings = find_python_files_and_listings(markdown_content)
    # for listing in listings:
    #     print(listing)
    update_markdown_listings(markdown_content, listings)
    sys.exit(0)

    updated_content = []
    for listing in listings:
        if listing.source_file:
            python_content = listing.source_file.read_text()
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
    console.print("Markdown file updated successfully!")


if __name__ == "__main__":
    main()