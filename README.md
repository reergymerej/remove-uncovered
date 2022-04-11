Remove code when it is not covered.
$ ptw --afterrun "python src/delete_uncovered/remove.py" -- --cov --cov-config=src/.coveragerc --cov-report xml

## TODO
* If there is an error during collection, do not run.  Coverage will be borked.
* It's possible we could break the source by commenting out the only line in a block.

    def foo():
      # crap
