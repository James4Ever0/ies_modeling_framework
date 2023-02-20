output_index_file = "processed_index.docx"
output_article_file = "processed_article.docx"

basepath = "../"
import os

master_path = os.path.join(basepath, output_index_file)
append_path_1 = os.path.join(basepath, output_article_file)
combined_path = os.path.join(basepath, "combined.docx")


from docxcompose.composer import Composer
from docx import Document

master = Document(master_path)
master.add_page_break() # working?
composer = Composer(master)

# but these hyperlinks are broken. it is the same in the original conversion, even if you do nothing just converting the html generated by pdoc3 using pandoc.

doc1 = Document(append_path_1)

composer.append(doc1)
composer.save(combined_path)

# no newpage avaliable?