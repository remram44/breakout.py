breakout.py -- drop to debugger when given output is written.

Usage
-----

Ever wondered where that weird-looking console output comes from? Simply run your program with breakout.py, and it will break to the debugger when the given text gets emitted. Useful to find sources of warnings, left over print statements, etc.

To use breakout.py, simply run it instead of the python binary::

    python breakout.py -t "error message" myscript.py arg1 arg2

The ``-m`` flag is also supported::

    python breakout.py -t "error message" -m mylib.entry_point arg1 arg2

If you install breakout.py via pip, note that you can run it from anywhere using ``python -m breakout ...``.
