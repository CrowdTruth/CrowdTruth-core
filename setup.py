from setuptools import setup, find_packages
import sys, os

setup(name='crowdtruth',
    version='2.0',
    description="Disagreement based metrics for the processing and evaluation of crowdsourced annotations",
    long_description="CrowdTruth is an approach to machine-human computing for collecting annotation data on text, images and videos. The approach is focussed specifically on collecting annotation data by capturing and interpreting inter-annotator disagreement. ",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic'],
    keywords=['CrowdTruth','crowdsourcing','disagreement','metrics','crowdflower','amazon mechanical turk'],
    author='Vrije Universiteit Amsterdam',
    author_email='crowdwatson@gmail.com',
    url='http://crowdtruth.org',
    license='Apache 2.0',
    download_url = 'https://github.com/CrowdTruth/CrowdTruth-core/archive/v2.0.tar.gz',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        'pymodm>=0.3.0',
        'pandas>=0.23.1'
        ],
    setup_requires=[],
    entry_points="""
        [console_scripts]
        CrowdTruth = crowdtruth:CrowdTruth
    """,
    )
