# Language identification #

## Description ##

The programme trains unigram language models for eleven European languages (Bulgarian, Czech, Danish, German, Greek, English, Spanish, Finnish, French, Hungarian and Portuguese) based on the parallel corpus from EuroParl. Each training set contains 10000 sentences.
To evaluate the language of a given document, the programme compares the profile of each language with the profile of the document and chooses the most similar one.
It outputs to the screen the language of the document and a sorted ranking of all competing languages.

## Usage ##
Basic usage:
```
python language_identification.py <input.txt>
```
