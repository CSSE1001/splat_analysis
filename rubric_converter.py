from criteria_checker import FAIL

MAJOR = "major"
MINOR = "minor"

class RubricConverter:

    def __init__(self, rubric, static_res):
        self._rubric = rubric
        self._static_res = static_res


    def convert(self):
        res = {}
        for criterion in self._rubric:

            fails = {MAJOR: 0, MINOR: 0}
            for rule in self._rubric[criterion]['rules']:
                if self._static_res[rule]['status'] == FAIL:
                    fails[self._rubric[criterion]['rules'][rule]] += 1

            score = 0
            for acceptable in self._rubric[criterion]['acceptable']:
                if self.is_acceptable(fails, acceptable):
                    score = acceptable['score']
                    break
            res[criterion] = score
        self._results = res

    @staticmethod
    def is_acceptable(fails, acceptable):
        for severity in fails:
            if fails[severity] > acceptable[severity]:
                return False
        return True

    def get_results(self):
        return self._results
