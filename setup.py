from setuptools import setup
import os


def read_requirements():
    here = os.path.dirname(os.path.abspath(__file__))
    req_path = os.path.join(here, 'requirements.txt')
    with open(req_path, 'r') as f:
        return f.read().splitlines()

def read_long_description():
    here = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(here, 'README.md')
    with open(readme_path, 'r', encoding='utf-8') as f:
        return f.read()


requirements = read_requirements()


setup(
    name='pose-estimation-recognition-utils',
    version='0.4.1',
    packages=['pose_estimation_recognition_utils'],
    install_requires=requirements,
    url='https://github.com/cobtras/pose-estimation-recognition-utils',
    license='Apache 2.0',
    author='Jonas David Stephan, Chanyut Boonkhamsaen, Nathalie Dollmann',
    author_email='j.stephan@system-systeme.de',
    description='Classes for AI recognition on pose estimation data',
    long_description=read_long_description(),          # README.md Inhalt
    long_description_content_type='text/markdown',
)
