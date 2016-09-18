from os.path import join

from setuptools import setup, find_packages
from os.path import dirname, join


setup(name='mlmonitor',
    version='0.3',
    description="Universal monitoring plugin for MarkLogic",
    long_description=open(join(dirname(__file__), 'README.rst'), encoding='utf-8').read(),
    classifiers=['Programming Language :: Python',
                     'Development Status :: 3 - Alpha',
                     'Natural Language :: English',
                     'Environment :: Console',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: Apache Software License',
                     'Operating System :: OS Independent',
                     'Topic :: Software Development :: Libraries :: Python Modules'
                     ],
    keywords='',
    author='Overstory LLP',
    author_email='products@overstory.co.uk',
    url='https://github.com/overstory/ml-monitoring-plugin',
    license=open(join(dirname(__file__), 'LICENSE'), encoding='utf-8').read(),
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        ### Required to build documentation
        # "Sphinx >= 1.0",
        ### Required for testing
        # "nose",
        # "coverage",
        ### Required to function
        'cement',
        'requests'
        ],
    setup_requires=[],
    entry_points="""
        [console_scripts]
        module = mlmonitor.cli.main:main
    """,
    namespace_packages=[],
    )
