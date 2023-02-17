ipconfig | rg 192.168
# python -m pydoc -n 0.0.0.0 -p 8001 .\cpExample.py

# pdoc and pdoc3 are different.
# i use pdoc.

# pdoc3 syntax
# pdoc --http 0.0.0.0:8001 .\cpExample.py
# pdoc --http 0.0.0.0:8001 .\example_docstring.py

# pdoc syntax
pdoc --port 8001 --search .\example_docstring.py