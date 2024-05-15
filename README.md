# Functional Error Handling
Code for Bruce Eckel's Pycon2024 Presentation

- The [slides for the presentation](https://github.com/BruceEckel/functional_error_handling/blob/main/Slides.md), in Markdown for presentation through [Obsidian](https://obsidian.md/).

- [Example source code](https://github.com/BruceEckel/functional_error_handling/tree/main/src/functional_error_handling). Presentation order:
    - [example1.py](https://github.com/BruceEckel/functional_error_handling/blob/main/src/functional_error_handling/example1.py)
    - [example2.py](https://github.com/BruceEckel/functional_error_handling/blob/main/src/functional_error_handling/example2.py)
    - [Result.py](https://github.com/BruceEckel/functional_error_handling/blob/main/src/functional_error_handling/result.py)
    - [example3.py](https://github.com/BruceEckel/functional_error_handling/blob/main/src/functional_error_handling/example3.py)
    - [example4.py](https://github.com/BruceEckel/functional_error_handling/blob/main/src/functional_error_handling/example4.py)
    - [result_with_bind.py](https://github.com/BruceEckel/functional_error_handling/blob/main/src/functional_error_handling/result_with_bind.py)
    - [example5.py](https://github.com/BruceEckel/functional_error_handling/blob/main/src/functional_error_handling/example5.py)
    - [example6.py](https://github.com/BruceEckel/functional_error_handling/blob/main/src/functional_error_handling/example6.py)

- The associated paper (a work in progress, which I think may eventually become part of a larger work) is [here](https://github.com/BruceEckel/functional_error_handling/blob/main/Functional%20Error%20Handling.md). Note that this is only partially done and needs significant rewriting.

- Works with [rye](https://rye-up.com/). Install rye, clone this repository, and run `rye sync` inside the home directory of the repository.

- Test with `rye test` (or `python -m pytest`, but not `pytest`).
