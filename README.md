# quordle-solver

To use, run `python3 gen_combos.py` to generate the required precomputed values. I recommend
using `pypy3` to do this.

Then, simply run `python3 play.py`.

Idea is a simple extension of 3Blue1Brown's idea of using information theory to solve Wordle.

Possible improvements:
* Calculate expected score rather than entropy as a metric for guess quality.
