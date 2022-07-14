from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fr:
    requirements = fr.read().splitlines()

setup(
    name='requiam_csv',
    version='0.13.0',
    packages=['requiam_csv'],
    url='https://github.com/UAL-RE/ReQUIAM_csv',
    license='MIT License',
    author='Yan Han',
    author_email='yhan818@gmail.com',
    description='Construct list of research themes and organization mapping to work with figshare patron management',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements
)
