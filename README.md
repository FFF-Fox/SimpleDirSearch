# SimpleDirSearch: A minimal directory search engine


## This is a simple search engine that you can use to search for terms, within the documents of a specified directory.

### Uses:
  - Run the search engine in a CLI, where you can try subsequent searches.
  ```
  $ python dir_search_engine.py
  ```

  - Search in the files of a specified directory using ```-d <directory>```.
  ```
  $ python dir_search_engine.py -d DocumentCollection
  ```
  - Run a single search for the given query term and return the results with ```-q <query>```
  ```
  $ python dir_search_engine.py -d DocumentCollection -q Query
  ```

### This is a work in progress.
Currently one can search using a single term. There will be an implementation of a boolean search model, where one will be able to search using AND, OR, and NOT to make more sophisticated queries.
