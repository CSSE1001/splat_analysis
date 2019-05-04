import sys
import json

from splat_analysis.analyser import Analyser
from pathlib import Path

SUBMISSION_FILES = ('event_decision.py', 'prediction.py')

ARG_OPTIONS = {
    '-static': 'get_static_results',
    '-messages': 'get_static_messages',
    '-rubric': 'get_rubric_data'
}

def splat_analysis_cli():
    """
    usage: splat_analysis path_to_submission (-static | -messages | -rubric)

    will save static_results.json, static_messages.json and
    suggested_programming_constructs.json to submission_dir
    """
    args = sys.argv[1:]
    if len(args) != 2:
        print('Incorrect args - usage: splat_analysis path_to_submission_dir (-static | -messages | -rubric | -all)')
        return 1

    sources = {}

    submission_dir_path = Path(args[0])
    files = [(name, (submission_dir_path / name)) for name in SUBMISSION_FILES]
    
    #read in files into sources
    for file_name, file_path in files:
        try:
            with open(file_path) as sub_file:
                sources[file_name] = sub_file.read()
        except IOError:
            print('Error trying to read file at address:', file_path)
            return 2

    analyser = Analyser(sources)
    analyser.analyse()
    


    if args[1] == '-all':
        data = {key[1:]: getattr(analyser, method)() for key, method in ARG_OPTIONS.items()}
    else:
        method = ARG_OPTIONS[args[1]]
        data = getattr(analyser, method)()
    
    print(json.dumps(data, sort_keys=True, indent=4))
    return 0

if __name__ == "__main__":
    splat_analysis_cli()
    

