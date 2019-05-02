from setuptools import setup

setup(
   name='splat_analysis',
   version='1.0',
   description='Static analysis for marking assignments',
   author='Rudi Scarpa',
   author_email='rudiscarpa96@gmail.com',
   packages=['splat_analysis'],
   install_requires=['radon', 'astor'],
)