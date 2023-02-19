from bs4 import BeautifulSoup as bs

input_file = "example_docstring.html"
output_file = "processed.html"

output_index_file = "processed_index.html"
output_article_file = "processed_article.html"
with open(input_file, "r") as f, open(output_file, "w+") as fw, open(
    output_index_file, "w+"
) as fw_index, open(output_article_file, "w+") as fw_article:
    soup = bs(f.read(), "lxml")
    # how about let's split the sidebar and main content into different pages?
    footer = soup.find(id="footer").extract()
    for details in soup.find_all("details"):
        details.extract()  # remove source code.
    # footer.clear()
    # print('footer?',footer)
    # breakpoint()
    sidebar = soup.find(id="sidebar").extract()
    soup.find(id="content").insert_before(sidebar)
    fw.write(str(soup.prettify()))
    # well let's split.
    # after done for the index.
    article = soup.find("article").extract()
    sidebar = soup.find(id="sidebar").extract()
    main = soup.find("main")
    main.insert(0,sidebar)
    fw_index.write(str(soup.prettify()))
    soup.find(id="sidebar").extract()
    title = soup.find("title").extract()  # removing the title.
    main.insert(0,article)  # insert the article
    fw_article.write(str(soup.prettify()))
