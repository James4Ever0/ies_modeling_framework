pandoc --metadata=title:"MyProject Documentation"  --from=markdown+abbreviations+tex_math_single_backslash  --pdf-engine=xelatex --variable=mainfont:"DejaVu Sans"   --toc --toc-depth=4 --output=example_docstring.pdf  example_docstring.md