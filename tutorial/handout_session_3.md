# Session 3: Data Processing & CrowdTruth Metrics

## Session Summary

In this session we discussed about optimal ways for representing and analyzing crowdsourcing results by applying the CrowdTruth metrics. We have prepared of collection of Jupyter Notebooks (also available as Colab notebooks that can be run from a Google Drive account) that illustrate how to run the metrics on the tasks discussed in [Session 2](handout_session_2.md):

**Closed Tasks:** the crowd picks from a set of annotations that is known beforehand

* **Binary Choice:** the crowd picks 1 annotation out of 2 choices (e.g. `True` and `False`)
    + **Person identification in videos**: [task template](img/ann-vec/bin-person-in-vid.pdf) | [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Binary%20Choice%20Task%20-%20Person%20Identification%20in%20Video.ipynb) | [Colab notebook](https://colab.research.google.com/drive/1ycZZdEDAPPzZ-uHYgtBfIzOcc8Sjebvx)
    + **Relation extraction in sentences**: [task template](img/ann-vec/bin-relex.pdf) | [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Binary%20Choice%20Task%20-%20Relation%20Extraction.ipynb) | [Colab notebook](https://colab.research.google.com/drive/1LQ6ndS0UC_IfUfGXr9d_B8hu7BlefKcy)
* **Ternary Choice:** the crowd picks 1 annotation out of 3 choices, (e.g. `True`, `False` and `None/Other`)
    + **Person identification in videos**: [task template](img/ann-vec/tern-person-in-vid.pdf) | [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Ternary%20Choice%20Task%20-%20Person%20Identification%20in%20Video.ipynb) | [Colab notebook](https://colab.research.google.com/drive/1ADZalDRLe5N4Q7BxIiJEUG4lGGiQnR5c)
* **Multiple Choice:** the crowd picks multiple annotation out of a set list of choices that are *the same* for every input unit
    + **Person identification in videos**: [task template](img/ann-vec/mult-person-in-vid.pdf) | [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Multiple%20Choice%20Task%20-%20Person%20Type%20Annotation%20in%20Video.ipynb) | [Colab notebook](https://colab.research.google.com/drive/1pDUyO6bvDmfnmwp5Hp8dxzv8Ekrow4uk)
    + **Relation extraction in sentences**: [task template](img/ann-vec/mult-relex.pdf) | [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Multiple%20Choice%20Task%20-%20Relation%20Extraction.ipynb) | [Colab notebook](https://colab.research.google.com/drive/1yAs2am0IIn7HXr-T9Yzd6p2k1HX7yIrX)
* **Sparse Multiple Choice:** the crowd picks multiple annotation out of a set list of choices that are *different* across input units
    + **Person identification in videos**: [task template](img/ann-vec/sparse-person-in-vid.pdf) | [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Sparse%20Multiple%20Choice%20Task%20-%20Person%20Annotation%20in%20Video.ipynb) | [Colab notebook](https://colab.research.google.com/drive/1uL2ex9QyK_iZjQLQINvyzMmYobDNH8WF)
    + **Relation extraction in sentences**: [task template](img/ann-vec/mult-relex.pdf) | [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Sparse%20Multiple%20Choice%20Task%20-%20Relation%20Extraction.ipynb) | [Colab notebook](https://colab.research.google.com/drive/11UnAsJeL3KUEqieB1bYEy2PJJJJZo_xA)
    + **Event extraction in sentences**: [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Sparse%20Multiple%20Choice%20Task%20-%20Event%20Extraction.ipynb) | [Colab notebook](https://colab.research.google.com/drive/1_e6BnwltZ7LDhZDiHtq1LoVQVPrV96Hq)
    
**Open-Ended Tasks:** the crowd dynamically creates the list of annotations, or the set of annotations is too big to compute beforehand

* **Sparse Multiple Choice:** the crowd picks multiple annotation out of a set list of choices that are *different* across input units
    + **Event extraction in sentences**:  [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Sparse%20Multiple%20Choice%20Task%20-%20Event%20Extraction.ipynb) | [Colab notebook](https://colab.research.google.com/drive/1_e6BnwltZ7LDhZDiHtq1LoVQVPrV96Hq)
* **Open-ended extraction tasks:** the crowd creates different combinations of annotations based on the input unit
    + **Person identification by highlighting words in text**: [task template](img/ann-vec/od-extr-person-in-vid.pdf) | [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Dimensionality%20Reduction%20-%20Stopword%20Removal%20from%20Media%20Unit%20%26%20Annotation.ipynb) | [Colab notebook](https://colab.research.google.com/drive/1oaJXaXO5zJaPyVHDwiRHVKVvkuva6Sj6)
    + **Event extraction by highlighting words in text**: [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Highlighting%20Task%20-%20Event%20Extraction.ipynb)
* **Free Choice:** the crowd inputs all possible annotations for an input unit
    + **Person identification in videos**: [task template](img/ann-vec/free-person-in-vid.pdf) | [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Free%20Input%20Task%20-%20Person%20Annotation%20in%20Video.ipynb) | [Colab notebook](https://colab.research.google.com/drive/1mvXr_b9ePUyGvBIgo1luRF3jCc6eMOpq)


## Session Excercises

1. [Install](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/getting_started.md#installation) the CrowdTruth package & follow the [How to run](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/getting_started.md#how-to-run) guide in order to get started.

2. Explore (some of) the notebooks above that implement CrowdTruth for different annotation tasks.

3. Compare the results of the CrowdTruth metrics when the same tasks is processed with a *closed vs. open-ended* annotation vector, by referring to the trade-off between the degree of expressivity in crowd annotations and potential for ambiguity and disagreement. The following notebook can be used as an example:
* Event extraction from sentences *(sparse multiple choice)*:
    + [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Sparse%20Multiple%20Choice%20Task%20-%20Event%20Extraction.ipynb)
    + [Colab notebook](https://colab.research.google.com/drive/1_e6BnwltZ7LDhZDiHtq1LoVQVPrV96Hq)

4. *Dimensionality reduction* techniques are useful to reduce some of the noise in crowd annotations, particularly for open-ended tasks as they produce very diverse labels. These techniques can be applied to both input units and annotations. Compare the results of the CrowdTruth metrics for an annotation task before & after dimensionality reduction in the following crowd tasks:

* Person identification by highlighting words in text *(open-ended extraction task)*:
    + [task template](img/ann-vec/od-extr-person-in-vid.pdf)
    + [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Dimensionality%20Reduction%20-%20Stopword%20Removal%20from%20Media%20Unit%20%26%20Annotation.ipynb)
    + [Colab notebook](https://colab.research.google.com/drive/1oaJXaXO5zJaPyVHDwiRHVKVvkuva6Sj6)
* Event extraction from sentences *(sparse multiple choice)*:
    + [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Sparse%20Multiple%20Choice%20Task%20-%20Event%20Extraction.ipynb)
    + [Colab notebook](https://colab.research.google.com/drive/1_e6BnwltZ7LDhZDiHtq1LoVQVPrV96Hq)
* Event extraction by highlighting words in text *(open-ended extraction task)*:
    + [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Highlighting%20Task%20-%20Event%20Extraction.ipynb)
* Person identification in videos *(free input task)*:
    + [task template](img/ann-vec/free-person-in-vid.pdf)
    + [Jupyter notebook](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Free%20Input%20Task%20-%20Person%20Annotation%20in%20Video.ipynb)
    + [Colab notebook](https://colab.research.google.com/drive/1mvXr_b9ePUyGvBIgo1luRF3jCc6eMOpq)
    
5. Implement the annotation vector you designed in [Session 2](handout_session_2.md) as a CrowdTruth pre-processing configuration.
