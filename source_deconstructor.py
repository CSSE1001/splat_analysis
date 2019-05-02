import ast
import astor
from pprint import pprint

GLB = 'global'
IMP = 'imports'
CLS = 'classes'
FUNC = 'functions'
MTHD = 'methods'

class SourceDeconstructor:
    def __init__(self, source):
        self._source = source
        self._res = {GLB: [],
                     IMP: [],
                     CLS: {},
                     FUNC: {}}

    def set_source(self, source):
        self._source = source

    def parse(self):
        tree = ast.parse(self._source)

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                self.parse_class(node)
            elif isinstance(node, ast.FunctionDef):
                self.parse_function(node)
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                self.parse_import(node)
            else:
                self.parse_global(node)

    def parse_class(self, node):
        # get name and stuff
        cname = node.name
        methods = {}
        cls = {'name': cname,
               'source': astor.to_source(node),
               MTHD: methods}

        # methods
        for child in node.body:
            if isinstance(child, ast.FunctionDef):
                mname = child.name
                method = {'name': mname,
                          'source': astor.to_source(child)}
                methods[mname] = method

        self.add_class(cname, cls)

    def add_class(self, cname, cls):
        self._res[CLS][cname] = cls

    def parse_function(self, node):
        fname = node.name
        source = astor.to_source(node)
        func = {'name': fname,
                'source': source}
        self.add_function(fname, func)

    def add_function(self, fname, func):
        self._res[FUNC][fname] = func

    def parse_import(self, node):
        source = astor.to_source(node)
        self.add_import(source)

    def add_import(self, source):
        self._res[IMP].append(source)

    def parse_global(self, node):
        source = astor.to_source(node)
        self.add_global(source)

    def add_global(self, source):
        self._res[GLB].append(source)

    def get_res(self):
        return self._res

def see_tree_nodes():
    with open(FILE) as file:
        source = file.read()
    tree = ast.parse(source)
    for node in tree.body:
        pprint(node)

if __name__ == '__main__':
    FILE = 'prediction.py'
    with open(FILE) as file:
        source = file.read()
    sd = SourceDeconstructor(source)
    sd.parse()
    res = sd.get_res()
    pprint(res)



