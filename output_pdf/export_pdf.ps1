$env:PATH+=$env:PATH;C:/Users/ss/scoop/apps/miktex/current/texmfs/install/miktex/bin/x64/

pandoc --metadata=title:"MyProject Documentation"  --from=markdown+abbreviations+tex_math_single_backslash  --pdf-engine=xelatex --variable=mainfont:"DejaVu Sans"   --toc --toc-depth=4 --output=example_docstring.pdf  example_docstring_utf8.md

# pandoc -s -o example_docstring.docx example_docstring.md