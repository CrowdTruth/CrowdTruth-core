from setuptools import setup, find_packages
import sys, os

setup(name='crowdtruth',
    version='1.1',
    description="Disagreement based metrics for the processing and evaluation of crowdsourced annotations",
    long_description="CrowdTruth is an approach to machine-human computing for collecting annotation data on text, images and videos. The approach is focussed specifically on collecting gold standard data for training and evaluation of cognitive computing systems. The original framework was inspired by the IBM Watson project for providing improved (multi-perspective) gold standard (medical) text annotation data for the training and evaluation of various IBM Watson components, such as Medical Relation Extraction, Medical Factor Extraction and Question-Answer passage alignment.",
    classifiers=[],
    keywords=['CrowdTruth','crowdsourcing','disagreement','metrics','crowdflower','amazon mechanical turk'],
    author='Vrije Universiteit Amsterdam',
    author_email='info@crowdtruth.org',
    url='http://crowdtruth.org',
    license='MIT',
    download_url = 'https://github.com/crowdtruth/crowdtruth-core/archive/v1.0.tar.gz',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        'pymodm>=0.3.0',
        'pandas'
        ],
    setup_requires=[],
    entry_points="""
        [console_scripts]
        CrowdTruth = crowdtruth:CrowdTruth
    """,
    )
