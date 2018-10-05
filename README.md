# ![CrowdTruth](http://crowdtruth.org/wp-content/uploads/2016/11/CrowdTruth.png)

[![PyPI version](https://badge.fury.io/py/CrowdTruth.svg)](https://badge.fury.io/py/CrowdTruth) [![Build Status](https://travis-ci.org/CrowdTruth/CrowdTruth-core.svg?branch=master)](https://travis-ci.org/CrowdTruth/CrowdTruth-core) [![codecov](https://codecov.io/gh/CrowdTruth/CrowdTruth-core/branch/master/graph/badge.svg)](https://codecov.io/gh/CrowdTruth/CrowdTruth-core) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/CrowdTruth/CrowdTruth-core/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/CrowdTruth/CrowdTruth-core/?branch=master) 

This library processes crowdsourcing results from Amazon Mechanical Turk and CrowdFlower following the CrowdTruth methodology. A full description of the metrics is available [in this paper](https://arxiv.org/abs/1808.06080). For more information see http://crowdtruth.org.

If you use this software in your research, please consider citing:

```
@article{CrowdTruth2,
  author    = {Anca Dumitrache and Oana Inel and Lora Aroyo and Benjamin Timmermans and Chris Welty},
  title     = {CrowdTruth 2.0: Quality Metrics for Crowdsourcing with Disagreement},
  year      = {2018},
  url       = {https://arxiv.org/abs/1808.06080},
}
```

Useful links:

* [Data](http://data.crowdtruth.org/) collected with CrowdTruth
* [Papers](http://crowdtruth.org/papers/) that use CrowdTruth
* Previous version [CrowdTruth v.1.0](https://github.com/CrowdTruth/CrowdTruth)


## Installation

To install the stable version from PyPI, install *pip* for your OS, then install package using:
```
pip install crowdtruth
```

To install the latest version from source, download the library and install it using:
```
python setup.py install
```

## Tutorial

The following tutorial is a collection of slides, exercises and Jupyter notebooks that explains what is the *CrowdTruth methodology*, and how to use it in practice. If you are already familiar with CrowdTruth, you can skip straight to the [guide on how to run this library](tutorial/getting_started.md).

### Introduction to CrowdTruth

* [Slides](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/Part%20I_%20CrowdTruth%20Tutorial.pdf)

### Task Design & Building CrowdTruth Annotation Vectors

* [Slides](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/Part%20II_%20CrowdTruth%20Tutorial.pdf)
* [Hands-on Exercises](tutorial/handout_session_2.md)

### Data Processing & CrowdTruth Metrics 

* [Slides](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/Part%20III_%20CrowdTruth%20Tutorial.pdf)
* [Getting Started with the CrowdTruth Library](tutorial/getting_started.md)
* [Hands-on Exercises](tutorial/handout_session_3.md)
