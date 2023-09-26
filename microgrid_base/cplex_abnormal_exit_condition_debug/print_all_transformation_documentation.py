from pyomo.environ import *
doc_dict = TransformationFactory._doc 
import inspect

for transform_name, transform_doc in doc_dict.items():
    cls = TransformationFactory._cls[transform_name]
    sourcefile_path = inspect.getsourcefile(cls)
    _, sourcelineno = inspect.getsourcelines(cls)
    print(f'name: {transform_name}')
    print(f'source: "{sourcefile_path}:{sourcelineno}"')
    # print(f'doc:')
    # class_doc = cls.__doc__
    # if class_doc is None:
    #     class_doc = transform_doc
    # for line in class_doc.split('\n'):
    #     print('\t'+line)
    print('doc:', transform_doc)
    print('='*60)