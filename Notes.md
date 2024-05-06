To turn off hovering for presentation, go to:
C:\Users\bruce\AppData\Roaming\Code\User\settings.json
And add:
    "editor.quickSuggestions": {
        "other": false,
        "comments": false,
        "strings": false
    },
    "editor.hover.enabled": false

- Functional programmers don't have the curse of knowledge, but the damnation of knowledge. It's amazing what they assume you know. Like concurrency, whatever niche they understand, they assume is obvious. (Their focus is figuring out functional programming, not communicating)

- The biggest thing that "introductory" functional programming tutorials assume you know is "why are we doing this." These tutorials most commonly devolve into a list of disparate features, without giving any unifying idea behind these features.

- Coconut seems to skip error handling altogether (it just uses exceptions)


----------------------------

Here's the markdown document I'm writing. Notice the information in the markdown comment:
<!-- #[code_location] ./src/functional_error_handling -->
This indicates that the source code examples are located relative to the current directory (./)
Can you create a python script that goes through my document and updates the python source-code listings from the python files in the code_location directory?
