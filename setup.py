from setuptools import find_packages, setup
from formstorm import __version__ as version_string
from os import path
import io


this_directory = path.abspath(path.dirname(__file__))
readme_path = path.join(this_directory, 'README.md')
with io.open(readme_path, encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='formstorm',
    version=version_string,
    url='https://github.com/TravisDart/formstorm/',
    description=(
        'FormStorm is a library that easily creates unit tests for Django '
        'forms.'
    ),
    license='MIT',
    author='Travis Dart',
    author_email='git@travisdart.com',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ],
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=["Django>=1.11"],
)
