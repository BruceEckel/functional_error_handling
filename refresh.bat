cd .\src\functional_error_handling\
rye test
python  .\update_output.py *
rye test
cd ..\..
python .\update_markdown_code_listings.py ".\Slides2.md"
python .\update_markdown_code_listings.py ".\Slides.md"
python .\update_markdown_code_listings.py ".\Functional Error Handling.md"
