input_file = "example_docstring.md"
output_file = "example_docstring_utf8.md"

with open(input_file,"r",encoding="utf-16") as f:
    with open(output_file,'w+',encoding='utf-8') as f8:
        f8.write(f.read())