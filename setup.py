from setuptools import find_packages, setup
from formstorm import __version__ as version_string


setup(
    name='formstorm',
    version=version_string,
    url='https://github.com/TravisDart/formstorm/',
    description=(
        'FormStorm is a Python library that easily creates unit tests for '
        'Django forms by defining valid/invalid values for each field.'
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
)
