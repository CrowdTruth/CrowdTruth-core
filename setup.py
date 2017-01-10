from setuptools import setup, find_packages
import sys, os

setup(name='CrowdTruth',
    version='0.1',
    description="CrowdTruth core application",
    long_description="CrowdTruth core application",
    classifiers=[],
    keywords='',
    author='Vrije Universiteit Amsterdam',
    author_email='b.timmermans@vu.nl',
    url='http://crowdtruth.org',
    license='MIT',
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
        'cement>=2.10.0',
        'pymodm>=0.3.0',
        'pandas'
        ],
    setup_requires=[],
    entry_points="""
        [console_scripts]
        CrowdTruth = crowdtruth:CrowdTruth
    """,
    namespace_packages=[],
    )
