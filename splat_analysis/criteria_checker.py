import splat_analysis.source_deconstructor as SD
import re

METRIC = 'metric'
NOT_EXISTS = 'not_exists'
CONTAINS = 'contains'
NOT_CONTAINS = 'not_contains'

PASS = 'pass'
FAIL = 'fail'
NA = 'not_attempted'

class CriteriaChecker:
    def __init__(self, static_data, criteria):
        self._static_data = static_data
        self._criteria = criteria
        self._results = None
        self._score = None

    def find_path(self, path):
        """returns data if dot separated path exists in the static data and False otherwise"""
        if '.' in path:
            try:
                cls, _, mthd = path.partition('.')
                return self._static_data[SD.CLS][cls][SD.MTHD][mthd]
            except KeyError:
                return False
        else:
            try:
                return self._static_data[SD.FUNC][path]
            except KeyError:
                try:
                    return self._static_data[SD.CLS][path]
                except KeyError:
                    return False

    def check(self):
        res = {}
        score = 0
        for c in self._criteria:
            data = self.find_path(c['location'])
            status = NA
            if data: #data exists
                status = FAIL
                if c['type'] == METRIC:
                    if self.check_metric(data, c):
                        score += 1
                        status = PASS
                elif c['type'] == CONTAINS:
                    if self.check_not_contains(data, c):
                        score += 1
                        status = PASS
                elif c['type'] == NOT_CONTAINS:
                    if self.check_contains(data, c):
                        score += 1
                        status = PASS
                elif c['type'] == NOT_EXISTS:
                    status = FAIL
                else:
                    raise ValueError(f"Unknown type for criteria: {c}")
            elif c['type'] == NOT_EXISTS:
                status = PASS

            res[c['name']] = {
                'name': c['name'],
                'location': c['location'],
                'status': status,
                'message': c['message']
            }
        self._results = res
        self._score = score

    def check_metric(self, data, c):
        return c['lower'] <= data[c['metric']] <= c['upper']

    def check_contains(self, data, c):
        return re.search(c['pattern'], data['source']) is not None

    def check_not_contains(self, source, kw):
        return not self.check_contains(source, kw)

    def get_results(self):
        return self._results

    def get_results_list(self):
        return [val for val in self._results.values()]

    def get_score(self):
        return self._score

if __name__ == '__main__':
    pass
    # cc = CriteriaChecker()
    # from pprint import pprint
    # pprint(cc._criteria)

