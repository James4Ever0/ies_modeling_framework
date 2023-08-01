import markdown

md = markdown.Markdown(extensions=["pymdownx.arithmatex"], output_format="html")


md.convertFile(input="jump_to_line.md", output="jump_to_line.html", encoding="utf-8")
