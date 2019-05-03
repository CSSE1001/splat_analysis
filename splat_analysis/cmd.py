import sys
import json

from splat_analysis.analyser import Analyser
from pathlib import Path

SUBMISSION_FILES = ('event_decision.py', 'prediction.py')

RESULT_PATHS = (
    ('get_static_results', 'static_results.json'),
    ('get_static_messages', 'static_messages.json'),
    ('get_rubric_data', 'suggested_programming_constructs.json')
)

# usage: splat_analysis path_to_submission

# will save static_results.json, static_messages.json and
# suggested_programming_constructs.json

def splat_analysis_cli():
    """
    usage: splat_analysis path_to_submission

    will save static_results.json, static_messages.json and
    suggested_programming_constructs.json to submission_dir
    """
    args = sys.argv[1:]
    if len(args) != 1:
        print('Incorrect args - usage: splat_analysis path_to_submission_dir')
        return 1

    sources = {}

    submission_dir_path = Path(args[0])
    files = [(name, (submission_dir_path / name)) for name in SUBMISSION_FILES]
    
    for sub_file_name, file_path in files:
        try:
            with open(files[sub_file_name]) as sub_file:
                sources[sub_file_name] = sub_file.read()
        except IOError:
            print('Error trying to read file at address:', 
                files[sub_file_name])
            return 2

    analyser = Analyser(sources)
    analyser.analyse()

    for method, file_path in RESULT_PATHS:
        try:
            with open((submission_dir_path / file_path), 'w') as result_file:
                data = getattr(analyser, method)()
                json.dump(data, result_file)
        except:
                print('Error trying to write results to:', result_file)
    return 0
    

