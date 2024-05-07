#: update_markdown_code_listings.py
import argparse
import difflib
import re
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pformat
from typing import List

from rich.console import Console

width = 65
console = Console()
python_files = []


@dataclass
class MarkdownListing:
    slugname: str
    markdown_listing: str
    source_file_path: Path | None
    # Exclude field from constructor arguments:
    source_file_contents: str = field(init=False)
    changed: bool = field(init=False)
    diffs: str = field(init=False)

    def __post_init__(self):
        if self.source_file_path is None:
            console.print(
                "[bold red] MarkdownListing: source_file_path not found among:[/bold red]"
            )
            console.print(pformat(python_files))
            raise ValueError("source_file cannot be None")
        self.source_file_contents = (
            "```python\n" + self.source_file_path.read_text(encoding="utf-8") + "```"
        )
        self.changed = self.markdown_listing != self.source_file_contents
        if self.changed:
            # Compute the differences between markdown_listing and source_file_contents
            differ = difflib.Differ()
            diff_lines = list(
                differ.compare(
                    self.markdown_listing.splitlines(keepends=True),
                    self.source_file_contents.splitlines(keepends=True),
                )
            )
            # Format the differences for display
            self.diffs = "".join(diff_lines)

    def __str__(self):
        return f"""
Filename from slugline: {self.slugname}
Source File: {self.source_file_path.absolute() if self.source_file_path else ""}
{self.changed = }
{"  Markdown Code Listing  ".center(width, "-")}[chartreuse4]
{self.markdown_listing}[/chartreuse4]
{"  Source File Code Listing  ".center(width, "-")}[chartreuse4]
{self.source_file_contents}[/chartreuse4]
{"  diffs  ".center(width,"v")}[chartreuse4]
{self.diffs}[/chartreuse4]
{'=' * width}
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
        listing_content = match.group(0)  # Include markdown tags
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
    updated_markdown = markdown_content
    for listing in listings:
        if not listing.changed:
            console.print(f"[bold green]{listing.slugname}")
        if listing.changed:
            console.print(f"[bold red]{listing.slugname}")
            console.print(f"[bright_cyan]{listing}")
            updated_markdown = updated_markdown.replace(
                listing.markdown_listing, listing.source_file_contents
            )
    return updated_markdown


def main():
    parser = argparse.ArgumentParser(
        description="Update Python slugline-marked source-code listings within a markdown file."
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
    updated_markdown = update_markdown_listings(markdown_content, listings)
    # sys.exit(0)
    markdown_file.write_text(updated_markdown, encoding="utf-8")
    console.print(f"{markdown_file} updated")


if __name__ == "__main__":
    main()
