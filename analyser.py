import json

import static_analyser as SA
import criteria_checker as CC
import rubric_converter as RC

class Analyser:
    def __init__(self, sources, criteria_path="marking_static_criteria.json", criteria=None, rubric_path="marking_rubric_convert.json", rubric=None):
        self._results = None
        self._sources = sources

        self._criteria_path = criteria_path
        self._criteria = criteria
        if criteria is None:
            self.load_criteria()

        self._rubric_path = rubric_path
        self._rubric = rubric
        if rubric is None:
            self.load_rubric()

    def load_criteria(self):
        with open(self._criteria_path) as file:
            self._criteria = json.load(file)

    def load_rubric(self):
        with open(self._rubric_path) as file:
            self._rubric = json.load(file)

    def set_sources(self, sources):
        self._sources = sources

    def analyse(self):
        static_res = {}
        score = 0

        # Static Criteria Analysis
        for file_name in self._sources:
            source = self._sources[file_name]

            # Breakdown source file and get static metrics
            sa = SA.StaticAnalyser(source)
            sa.analyse()
            static_data = sa.get_results()

            # Compare static metrics with stored criteria
            cc = CC.CriteriaChecker(static_data, self._criteria[file_name])
            cc.check()
            static_res.update(cc.get_results())
            score += cc.get_score()

        self._static_results = static_res
        self._score = score

        rc = RC.RubricConverter(self._rubric, static_res)
        rc.convert()
        self._rubric_data = rc.get_results()

    def get_static_results(self):
        return [val for val in self._static_results.values()]

    def get_static_messages(self):
        return [rule['message']
                for rule in self.get_static_results()
                if rule['status'] == CC.FAIL]

    def get_rubric_data(self):
        return self._rubric_data

    def get_score(self):
        return self._score

if __name__ == '__main__':
    pass
    sources = {}
    with open('prediction.py') as prediction, open('event_decision.py') as event:
        sources['prediction.py'] = prediction.read()
        sources['event_decision.py'] = event.read()

    from pprint import pprint
    a = Analyser(sources)
    a.analyse()
    # pprint(a.get_static_results())
    # pprint(a.get_static_messages())
    pprint(a.get_rubric_data())