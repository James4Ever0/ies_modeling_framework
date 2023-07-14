rm example_docstring.docx
python .\convert_utf8.py # use iconv instead. installed along with busybox.
pandoc example_docstring_utf8.md -o example_docstring.docx