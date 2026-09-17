"""
The Steup.py is used for packaging the project and Distributing. 
It is used by Setuptools to define the configuration of the project,
Such as dependencies and more.
"""
import os
import sys
from typing import List
from setuptools import find_packages,setup

def get_requirements()->List[str]:
    '''
    will be used to know the requirements(dependencies) for the project.
    all those folders with __init__.py will automatically considered a package to be used in other codes.
    '''
    requirement_list = []
    try:
        with open('requirements.txt','r') as file:
            #read lines from the file
            lines = file.readlines() #process each line
            for line in lines:
                requirements=line.strip()
                ## ignore the empty lines and -e .
                if requirements and requirements!='-e .':
                    requirement_list.append(requirements) 
    except FileNotFoundError:
        print('requirements.txt file not find')
    
    return requirement_list

setup(
    name='NetworkSequrity',
    version="0.0.1",
    author="Prateek Khicher",
    author_email='162597487+Prateekkhicher@users.noreply.github.com',
    packages=find_packages(),
    install_requires=get_requirements()
)