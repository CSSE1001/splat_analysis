from setuptools import setup

setup(
   name='splat_analysis',
   version='1.0',
   description='Static analysis for marking assignments',
   author='Rudi Scarpa',
   author_email='rudiscarpa96@gmail.com',
   packages=['splat_analysis'],
   install_requires=['radon', 'astor'],
   entry_points={
      'console_scripts': [
         'splat_analysis = splat_analysis.cmd:splat_analysis_cli'
      ]
   }
)