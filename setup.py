from setuptools import setup, find_packages
# import os
# import sys

setup(
    name='crowdtruth',
    version='2.1',
    description=
    "Disagreement based metrics for the processing and evaluation of crowdsourced annotations",
    long_description=
    ("CrowdTruth is an approach to machine-human computing for collecting annotation data on " +
     "text, images and videos. The approach is focussed specifically on collecting annotation" +
     " data by capturing and interpreting inter-annotator disagreement. "),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Information Analysis',
        # 'Topic :: Scientific/Engineering :: Crowdsourcing',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic'],
    keywords=['CrowdTruth', 'crowdsourcing', 'disagreement', \
                'metrics', 'crowdflower', 'amazon mechanical turk'],
    author='Vrije Universiteit Amsterdam',
    author_email='crowdwatson@gmail.com',
    url='http://crowdtruth.org',
    license='Apache 2.0',
    download_url='https://github.com/CrowdTruth/CrowdTruth-core/archive/2.1.zip',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='test',
    install_requires=[
        'pymodm>=0.3.0',
        'pandas>=0.23.1',
        'numpy>=1.13.3',
        'scipy>=1.0.0',
        'chardet>=3.0.4',
        'coverage>=4.5.1',
        'codecov>=2.0.15',
        'dateparser>=0.7.0'
        ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    entry_points="""
        [console_scripts]
        CrowdTruth = crowdtruth:CrowdTruth
    """,
    )
