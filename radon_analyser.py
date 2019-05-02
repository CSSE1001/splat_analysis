from radon.visitors import ComplexityVisitor
from radon.complexity import sorted_results
from radon.complexity import LINES

from radon.raw import analyze

from radon.metrics import h_visit

class RadonAnalyser:

    def __init__(self, source = ''):
        self._source = source
        self._res = {}

    def set_source(self, source):
        self._source = source

    def analyse(self):
        output = {}
        cv = ComplexityVisitor.from_code(self._source)
        res = sorted_results(cv.functions + cv.classes, order=LINES)
        # should be one result, since giving one function
        # if len(res) > 1:
        #     raise ValueError('Complexity Analysis returned multiple results')
        output['cc'] = res[0].complexity

        res = analyze(self._source)
        lines_comments = dict(res._asdict())
        output.update(lines_comments)

        res = h_visit(self._source)
        hals = dict(res._asdict())
        output.update(hals)

        self._res = output

    def get_res(self):
        return self._res

if __name__ == '__main__':
    from pprint import pprint
    FILE = 'python_sources/a1/a1_solution_encrypt.py'
    # FILE = 'python_sources/a2_test/init_function_test.py'
    with open(FILE) as filein:
        ra = RadonAnalyser(filein.read())
        ra.analyse()
        res = ra.get_res()
        pprint(res)