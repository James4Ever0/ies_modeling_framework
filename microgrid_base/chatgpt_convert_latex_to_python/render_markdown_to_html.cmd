@REM python -m markdown -f jump_to_line.html -o html jump_to_line.md
@REM https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/
@REM python render_markdown_with_latex.py

@REM pandoc -o jump_to_line.html jump_to_line.md
@REM markdown-it jump_to_line.md > jump_to_line.html
@REM npm install markdown-it markdown-it-mathjax3
node render_latex.js
@REM then pdf
@REM pandoc -o jump_to_line.pdf  jump_to_line.md
@REM pandoc -o jump_to_line.pdf  jump_to_line.html
playwright pdf jump_to_line.html jump_to_line.pdf