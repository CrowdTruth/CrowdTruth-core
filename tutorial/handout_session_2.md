# Handout Session 2: Task Design & Building the Annotation Vector

## Session Summary

In this session, we discussed a series of crowdsourcing tasks, with different methods of collecting the annotations from the workers. Below you can find a list of tasks (with their corresponding crowdsoursing templates):

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



## Task

Take either *one of the annotation tasks* presented, or *a task of your choice*, and transform the annotation vector, by doing one or several of the following:

* Redesigning the annotation task by:
    + Changing the type of the input unit (text vs. image vs. video)
    + Changing the way the crowd annotations are collected (radio boxes, checkboxes, free text, other)
* Adding/removing components of the annotation vector
* Merging/clustering existing components of the annotation vector

How will these changes affect the annotation vector of your crowdsourcing task? Describe the outcome in terms of the trade-off between the degree of expressivity in crowd annotations and potential for ambiguity and disagreement.

Create *slides for a 1 minute presentation* summarizing your new crowdsourcing task, annotation vector, and the possible ways for ambiguity to be expressed in it.
