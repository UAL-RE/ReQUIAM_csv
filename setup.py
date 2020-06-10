from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fr:
    requirements = fr.read().splitlines()

setup(
    name='DataRepository_research_themes',
    version='0.9.3',
    packages=find_packages('DataRepository_research_themes'),
    url='https://github.com/ualibraries/DataRepository_research_themes',
    license='MIT License',
    author='Chun Ly',
    author_email='astro.chun@gmail.com',
    description='Construct list of research themes and organization mapping to work with figshare patron management',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements
)
