import json

import splat_analysis.static_analyser as SA
import splat_analysis.criteria_checker as CC
import splat_analysis.rubric_converter as RC

class Analyser:
    def __init__(self, sources,
                 criteria_path="marking_static_criteria.json", criteria=None,
                 rubric_path="marking_rubric_convert.json", rubric=None):
        """
        The main entry class for the static analysis and friends. Should only
        need to access this class if all goes well.

        You should supply one of (criteria_path, criteria) and one of
        (rubric_path, rubric), otherwise can leave both blank to use
        the default files

        Parameters:
            {str: str} sources: Dictionary mapping file name to file contents
                    See '__main__' for example 
            (str) criteria_path: file path to criteria json
            (dict) criteria: dictionary of criteria json,
                        See 'marking_static_criteria.json' as an example
            (str) rubric_path: file path to rubric json
            (dict) rubric: dictionary of rubric json,
                        See 'marking_rubric_convert.json' as an example

        An example of usage is in the '__main__', but should basically
        look this:

        a = Analyser() #<-- can add arguments as necessary
        a.analyse() #<-- runs the analysis stuff and sets internal results

        #After analyse, use any of these methods to get data back
        a.get_static_results()
        a.get_static_messages()
        a.get_rubric_data()
        
        """
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
        """
        Returns a list of dictionaries corresponding to the criteria json used
        for analysis.

        Should end up looking like this:

        [
            {
                'name': 'unique_name_of_the_static_rule'
                'location': 'location_str'   #<-- eg. Event.__init__
                'status': 'pass' / 'fail' / 'not_attempted'
                'message': 'message to marker'
            },
            {...}
        ...
        ]
        """
        return [val for val in self._static_results.values()]

    def get_static_messages(self):
        """
        Returns a list of strings that contain all the filtered messages
        to display to the marker. Literally just filtered messages from
        the above method, based on which were failed
        """
        return [rule['message']
                for rule in self.get_static_results()
                if rule['status'] == CC.FAIL]

    def get_rubric_data(self):
        """
        Returns the suggested rubric based on the supplied rubric json as
        a dictionary. Should correspond to the 6 contruct criteria.
        For example, using marking_rubric_convert.json will return something
        like:

        {
            "program_structured_readable": 1,
            "identifier_names": 1,
            "algorithmic_logic": 1,
            "methods_well_designed": 1
            "difference_classes_instances": 1,
            "encapsulation_inheritance": 1
        }

        The keys of this dictionary are determined by the top level names
        in the rubric json

        Returns:
            {str: float}
        """
        return self._rubric_data

    def get_score(self):
        return self._score

# if __name__ == '__main__':
#     sources = {}
#     with open('prediction.py') as prediction, open('event_decision.py') as event:
#         sources['prediction.py'] = prediction.read()
#         sources['event_decision.py'] = event.read()

#     from pprint import pprint
#     a = Analyser(sources)
#     a.analyse()
    # pprint(a.get_static_results())
    # pprint(a.get_static_messages())
    # pprint(a.get_rubric_data())
