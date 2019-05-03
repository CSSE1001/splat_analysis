import splat_analysis.radon_analyser as RA
import splat_analysis.source_deconstructor as SD

class StaticAnalyser:
    def __init__(self, source = ''):
        self._source = source
        self._res = None

    def set_source(self, source):
        self._source = source

    def analyse(self):
        self._res = {}

        # break up source code into individual pieces
        sd = SD.SourceDeconstructor(self._source)
        sd.parse()
        parts = sd.get_res()

        # run static analysis on each part
        # classes
        if SD.CLS in parts:
            cls_analysis = {}
            for cls_name, cls in parts[SD.CLS].items():
                cls_analysis[cls_name] = self.analyse_class(cls)
            self._res[SD.CLS] = cls_analysis

        # global functions
        if SD.FUNC in parts:
            func_analysis = {}
            for func_name, func in parts[SD.FUNC].items():
                func_analysis[func_name] = self.analyse_function(func)
            self._res[SD.FUNC] = func_analysis

        # add analysis for imports/global code here if needed

    def analyse_class(self, cls):
        res = {}

        # analyse entire class source - most likely unused
        cls_source = cls['source']
        ra = RA.RadonAnalyser(cls_source)
        ra.analyse()
        res = ra.get_res()
        res['source'] = cls_source

        # analyse methods
        if SD.MTHD in cls:
            mthd_analysis = {}
            for mthd_name, mthd in cls[SD.MTHD].items():
                mthd_analysis[mthd_name] = self.analyse_function(mthd)
            res[SD.MTHD] = mthd_analysis

        return res

    def analyse_function(self, func):
        func_source = func['source']
        ra = RA.RadonAnalyser(func_source)
        ra.analyse()
        res = ra.get_res()
        res['source'] = func_source
        return res

    def get_results(self):
        return self._res

if __name__ == '__main__':

    FILE = 'event_decision.py'
    with open(FILE) as file:
        source = file.read()

    sa = StaticAnalyser(source)
    sa.analyse()
    res = sa.get_results()

    from pprint import pprint
    pprint(res)
