from setuptools import find_packages, setup
from formstorm import __version__ as version_string

setup(
    name='formstorm',
    version=version_string,
    url='https://github.com/TravisDart/formstorm/',
    description=(
        'A tool to test Django forms by trying (almost) every '
        'combination of valid and invalid input.'
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
        'Framework :: Django :: 1.11',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Testing',
    ],
    packages=find_packages(),
    include_package_data=True,
    # test_suite='nose.collector',
    tests_require=['django'],
)
