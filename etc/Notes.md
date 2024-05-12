1. Change 'value' field to 'answer' in Result
2. Should there be a success(self) method?
3. Search all text for Ok and Err
4. Does Returns have and_then? If so could use that earlier and avoid repetition of definitions of func_a etc. If it's named something else we could use that in result.py

https://sobolevn.me/2019/02/python-exceptions-considered-an-antipattern

VSCode next/previous tab Ctrl-PgDown/Ctrl-PgUp

To turn off hovering for presentation, go to:
C:\Users\bruce\AppData\Roaming\Code\User\settings.json
And add:
    "editor.quickSuggestions": {
        "other": false,
        "comments": false,
        "strings": false
    },
    "editor.hover.enabled": false


- Coconut seems to skip error handling altogether (it just uses exceptions)


----------------------------

For eventual use as documentation for update_markdown_code_listings.py

I want to create a tool to update the python source-code listings within a markdown file. The listings in the markdown file look like this:

```python
#: name_of_python_file.py
(rest of listing)
```

So these listings are bounded by triple back-ticks, and each python listing begins with "```python". The first line of each listing is a "slug line" that
starts with "#:" and the remainder of that line is the file name of the current listing.

The python files that are used to update these files also begin with a slug line. This will be identical to the slug line in the associated listing in the markdown file.

To locate the python files used to update the listings, the markdown file will contain one or more markdown comments of the form:
<!-- #[code_location] ./path/to/python/files -->
This indicates that the source code examples are located relative to the current directory (./), but a path can also be absolute.

Here's how I can imagine approaching this problem:
1. Find all the #[code_location] path(s) in the markdown file.
2. Create a list of all the python files located in those paths.
3. Move through the markdown file finding all the listings starting with ```python and ending with ``` which also contain slug lines.
4. For every listing that contains a slug line, find the associated python file on disk, with the file name indicated in the slug line and verify that there is also a correct slug line in the file.
5. Compare the contents of the file on disk with the contents of the listing in the markdown file. If the contents are the same, do nothing and indicate that no change was made for that particular listing. If the contents differ, update the listing in the markdown file from the contents of the python file on disk, and indicate that a change was made for that particular listing.
