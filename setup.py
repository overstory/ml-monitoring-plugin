import io
from os.path import dirname, join

from setuptools import setup, find_packages

setup(name='mlmonitor',
      version='0.3',
      description="Universal monitoring plugin for MarkLogic",
      long_description=io.open(join(dirname(__file__), 'README.md'), encoding='utf-8').read(),
      classifiers=['Programming Language :: Python',
                   'Development Status :: 3 - Alpha',
                   'Natural Language :: English',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7'
                   ],
      keywords='',
      author='Overstory LLP',
      author_email='products@overstory.co.uk',
      url='https://github.com/overstory/ml-monitoring-plugin',
      license=io.open(join(dirname(__file__), 'LICENSE'), encoding='utf-8').readline().strip(),
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      package_data={
          'mlmonitor': ['config/endpoints.yml'],
      },
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=[
          ### Required to build documentation
          # "Sphinx >= 1.0",
          ### Required for testing
          # "nose",
          # "coverage",
          # "bottle",
          ### Required to function
          'cement',
          'requests',
          'enum34',
          'pyYaml',
          'isodate'
      ],
      setup_requires=[],
      entry_points="""
        [console_scripts]
        mlmonitor = mlmonitor.cli.main:main
    """,
      namespace_packages=[],
      )
