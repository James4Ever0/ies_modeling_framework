mytext = """
my text with some keywords
my text with some keywords
my text with some keywords
my text with some keywords
my_variable_with_index[0]
"""

import flashtext

# you may use two different views, one is the element view, another is the array view.
# array view is simply done by removing bracket enclosed indexes from variable names.

keyword_processor = flashtext.KeywordProcessor()
keyword_processor.add_keyword('keywords')
keyword_processor.add_keyword('with')
keywords_found = keyword_processor.extract_keywords(mytext)
print(keywords_found)

keyword_counts = {}
for keyword in keywords_found:
    keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1

print(keyword_counts)