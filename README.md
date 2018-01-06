# Information Retrieval codebase

## Contains implementations of models and other IR specific algorithms.

## boolean_engine.py: This is a simple search engine (based on the boolean retrieval model) that you can use to search for terms contained in the documents of a specified directory/collection.

### Uses:
  - Run the search engine in a CLI, where you can try subsequent searches.
  ```
  $ python boolean_engine.py
  ```

  - Search in the files of a specified directory using ```-d <directory>```.
  ```
  $ python boolean_engine.py -d DocumentCollection
  ```
  - Search the subdirectories of the specified directory as well ```-rf```
  ```
  $ python boolean_engine.py -d DocumentCollection -rf
  ```

### This is a work in progress.
You can search using many terms separated by ```&```, ```|``` for logical AND, OR respectively and use ```!``` before a term to specify negation of the term. eg: ```Search: term1 & term2 | !term3```. The query is expressed using conjuctive normal form.
