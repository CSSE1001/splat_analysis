# splat_analysis

Using the stuff locally should be pretty simple.

Firstly, you'll need install a few python dependencies on your environment

radon: https://pypi.org/project/radon/
astor: https://pypi.org/project/astor/

For me was:
    pip install radon
    pip install astor

pylint was giving me the business for some reason so I might add that in
later but for now I believe that's it for dependencies


Using it is real simple, you should only need to access the Analyse class
from analyse.py. The class & methods you need to use are documented in that
file and there's an example commented out down the bottom. But basically you
need to create an Analyser instance, have it proces the relevant files, then
get the data back.

Will probs look something like this (again, more detailed in analysis.py):

    ...
    sources = {}
    with open('prediction.py') as prediction, open('event_decision.py') as event:
        sources['prediction.py'] = prediction.read()
        sources['event_decision.py'] = event.read()


    a = Analyser(sources)
    a.analyse()

    a.get_static_results()
    a.get_static_messages()
    a.get_rubric_data()
    ...

A final thing is that I set up my internal imports as if they're all the in the
source folder. I don't know how you stuff is set up but you may need to edit those
imports so they work relative to your project source