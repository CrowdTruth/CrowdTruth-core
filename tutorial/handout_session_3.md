# Handout Session #3: Data Processing & CrowdTruth metrics

## Session Summary

In this session we discussed about optimal ways for representing and analyzing crowdsourcing results by applying the CrowdTruth metrics.

**Closed Tasks:** the crowd picks from a set of annotations that is known beforehand

* **Binary Choice:** the crowd picks 1 annotation out of 2 choices (e.g. `True` and `False`)
    + *e.g.:* [Person identification in videos](img/ann-vec/bin-person-in-vid.pdf), [Relation extraction from sentences](img/ann-vec/bin-relex.pdf)
* **Ternary Choice:** the crowd picks 1 annotation out of 3 choices, (e.g. `True`, `False` and `None/Other`)
    + *e.g.:* [Person identification in videos](img/ann-vec/tern-person-in-vid.pdf)
* **Multiple Choice:** the crowd picks multiple annotation out of a set list of choices that are *the same* for every input unit
    + *e.g.:* [Person identification in videos](img/ann-vec/mult-person-in-vid.pdf), [Relation extraction from sentences](img/ann-vec/mult-relex.pdf)
* **Sparse Multiple Choice:** the crowd picks multiple annotation out of a set list of choices that are *different* across input units
    + *e.g.:* [Person identification in videos](img/ann-vec/sparse-person-in-vid.pdf), [Relation extraction from sentences](img/ann-vec/mult-relex.pdf), Event extraction from sentences
    
**Open-Ended Tasks:** the crowd dynamically creates the list of annotations, or the set of annotations is too big to compute beforehand

* **Sparse Multiple Choice:** the crowd picks multiple annotation out of a set list of choices that are *different* across input units
    + *e.g.:* Event extraction from sentences
* **Open-ended extraction tasks::** the crowd creates different combinations of annotations based on the input unit
    + *e.g.:* [Person identification by highlighting words in text](img/ann-vec/od-extr-person-in-vid.pdf)
* **Free Choice:** the crowd inputs all possible annotations for an input unit
    + *e.g.:* [Person identification in videos](img/ann-vec/free-person-in-vid.pdf)


## Session Excercises

1. Install the CrowdTruth package & follow the **How to run** guide in order to get started.
2. Explore (some of) the notebooks implementing CrowdTruth for different annotation tasks
* **Binary choice tasks:** the crowd picks 1 annotation out of 2 choices (e.g. `True` and `False`)
    + [Person identification in videos](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Binary%20Choice%20Task%20-%20Person%20Identification%20in%20Video.ipynb)    
    + [Relation extraction from sentences](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Binary%20Choice%20Task%20-%20Relation%20Extraction.ipynb)

* **Ternary choice tasks:** the crowd picks 1 annotation out of 3 choices, (e.g. `True`, `False` and `None/Other`)
    + [Person identification in videos](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Ternary%20Choice%20Task%20-%20Person%20Identification%20in%20Video.ipynb)

* **Multiple choice tasks:** the crowd picks multiple annotation out of a set list of choices that are *the same* for every input unit
    + [Person identification in videos](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Multiple%20Choice%20Task%20-%20Person%20Type%20Annotation%20in%20Video.ipynb)
    + [Relation extraction from sentences](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Multiple%20Choice%20Task%20-%20Relation%20Extraction.ipynb)

* **Sparse multiple choice tasks:** the crowd picks multiple annotation out of a set list of choices that are *different* across input units
    + [Person identification in videos](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Sparse%20Multiple%20Choice%20Task%20-%20Person%20Annotation%20in%20Video.ipynb)
    + [Relation extraction from sentences](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Sparse%20Multiple%20Choice%20Task%20-%20Relation%20Extraction.ipynb)
    + [Event extraction from sentences](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Sparse%20Multiple%20Choice%20Task%20-%20Event%20Extraction.ipynb)

* **Open-ended extraction tasks:** the crowd creates different combinations of annotations based on the input unit (e.g. extracting named entities from a paragraph, identifying objects in an image by drawing bounding boxes)
    + [Person identification by highlighting words in text](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Dimensionality%20Reduction%20-%20Stopword%20Removal%20from%20Media%20Unit%20%26%20Annotation.ipynb)
    + [Event extraction by highlighting words in text](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Highlighting%20Task%20-%20Event%20Extraction.ipynb)

* **Free input:** the crowd inputs all possible annotations for an input unit
    + [Person identification in videos](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Free%20Input%20Task%20-%20Person%20Annotation%20in%20Video.ipynb)


3. Compare the results of the CrowdTruth metrics for an annotation task before & after dimensionality reduction. The following notebooks can be used as example:

* **Sparse multiple choice tasks:** the crowd picks multiple annotation out of a set list of choices that are *different* across input units
    + [Event extraction from sentences](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Sparse%20Multiple%20Choice%20Task%20-%20Event%20Extraction.ipynb)

* **Open-ended extraction tasks:** the crowd creates different combinations of annotations based on the input unit (e.g. extracting named entities from a paragraph, identifying objects in an image by drawing bounding boxes)
    + [Person identification by highlighting words in text](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Dimensionality%20Reduction%20-%20Stopword%20Removal%20from%20Media%20Unit%20%26%20Annotation.ipynb)
    + [Event extraction by highlighting words in text](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Highlighting%20Task%20-%20Event%20Extraction.ipynb)

* **Free input:** the crowd inputs all possible annotations for an input unit
    + [Person identification in videos](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Free%20Input%20Task%20-%20Person%20Annotation%20in%20Video.ipynb)

4. Compare the results of the CrowdTruth metrics for an open vs. closed task. The following notebook can be used as an example:
* **Sparse multiple choice tasks:** the crowd picks multiple annotation out of a set list of choices that are *different* across input units
    + [Event extraction from sentences](https://github.com/CrowdTruth/CrowdTruth-core/blob/master/tutorial/notebooks/Sparse%20Multiple%20Choice%20Task%20-%20Event%20Extraction.ipynb)
    
5. Implement the annotation vector you designed in [Session 2](https://raw.githubusercontent.com/CrowdTruth/CrowdTruth-core/master/tutorial/handout_session_2.md) as a CrowdTruth pre-processing configuration.
