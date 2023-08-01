# import markdown

# md = markdown.Markdown(extensions=["pymdownx.arithmatex"], output_format="html")

# md.convertFile(input="jump_to_line.md", output="jump_to_line.html", encoding="utf-8")

from markdown_it import MarkdownIt
from mdit_py_plugins import dollarmath

md = MarkdownIt().use(dollarmath)

sample_markdown=r"""
# hello latex
$$
\alpha = \beta
$$
"""

html_string = md.render(sample_markdown)
print(html_string)