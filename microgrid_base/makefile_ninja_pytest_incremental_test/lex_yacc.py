class LexMeta(type):
    def __new__(cls, name, bases, cdict):
        tokens = []
        # unprocessed_tokens = []
        skipped_tokens = []
        for attrName, attr in cdict.items():
            # for parser starting with "p_"
            assert not attrName.startswith(
                "t_"
            ), f"Wrong attribute name: {attrName}\nShall not start any attribute with 't_'!"
            # if attrName.startswith("t_"):
            #    unprocessed_tokens.append(attrName)
            splitedAttrName = list(filter(lambda e: len(e) > 0, attrName.split("_")))
            if len(splitedAttrName) > 0:
                indicator = splitedAttrName[-1][0]
                if indicator.upper() == indicator and indicator.lower() != indicator:
                    tokens.append(attrName)
            else:
                skipped_tokens.append(attrName)
        cdict["tokens"] = tokens
        for token in tokens + skipped_tokens:
            cdict[f"t_{token}"] = cdict.pop(token)
        return super(LexMeta, cls).__new__(cls, name, bases, cdict)


import ply.lex as lex


class sampleLex(metaclass=LexMeta):
    ID = r"\w+"

    def build(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)


myLex = sampleLex()
print(dir(sampleLex))
print(dir(myLex))

import ply.yacc as yacc

# be it a class?

myParser = yacc.yacc(module = myModule)
