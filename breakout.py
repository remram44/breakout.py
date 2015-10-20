#!/usr/bin/env python
from __future__ import absolute_import, division

import argparse
import locale
import pdb
import re
import runpy
import sys


__version__ = '0.1'


PY3 = sys.version_info[0] == 3


class BreakingStream(object):
    """Stream replacement that will break on the given patterns.
    """
    __buffer_size = 1024

    def __init__(self, stream, text, regex):
        self.__stream = stream
        self.__text = list(text)
        self.__regex = [re.compile(s) for s in regex]
        self.__buffer = ''
        self.__ignore = False

    def write(self, obj):
        self.__stream.write(obj)
        if self.__ignore:
            return
        # If it doesn't raise...
        if PY3:
            if isinstance(obj, bytes):
                obj = obj.decode('utf-8', 'replace')
        else:
            if isinstance(obj, unicode):
                obj = obj.encode('utf-8')
        lines = iter(obj.splitlines(True))
        line = next(lines)
        line = self.__buffer[:self.__buffer_size - len(line)] + line
        self._line(line)
        for line in lines:
            self._line(line)
        self.__buffer = line

    def _line(self, line):
        for t in self.__text:
            if t in line:
                self.__ignore = True
                pdb.set_trace()
        for r in self.__regex:
            if r.search(line) is not None:
                self.__ignore = True
                pdb.set_trace()


def main():
    """Entry point when called on the command-line.
    """
    # Locale
    locale.setlocale(locale.LC_ALL, '')

    parser = argparse.ArgumentParser(
        description="breakout - drop to debugger when given output is written")
    parser.add_argument('--regex', '-r', nargs=1,
                        default=[],
                        help="Regular expression to break on")
    parser.add_argument('--text', '-t', nargs=1,
                        default=[],
                        help="Text output to break on")
    parser.add_argument('--stdout', action='store_true', default=False,
                        help="Only watch stdout")
    parser.add_argument('--stderr', action='store_true', default=False,
                        help="Only watch stderr")
    parser.add_argument('cmdline', nargs=argparse.REMAINDER,
                        help="Python script to execute")
    parser.add_argument('-m', dest='module', nargs=argparse.REMAINDER,
                        help="module name to execute")

    args = parser.parse_args()
    if not args.cmdline and not args.module:
        parser.error("Nothing to execute; please pass a script name or use -m")
        raise RuntimeError  # unreachable

    if args.stdout or args.stderr:
        stdout = args.stdout
        stderr = args.stderr
    else:
        stdout = stderr = True
    if stdout:
        sys.stdout = BreakingStream(sys.stdout,
                                    text=args.text, regex=args.regex)
    if stderr:
        sys.stderr = BreakingStream(sys.stderr,
                                    text=args.text, regex=args.regex)

    if args.module:
        sys.argv = args.module
        runpy.run_module(args.module[0], alter_sys=True)
    else:
        sys.argv = args.cmdline
        runpy.run_path(args.cmdline[0])


if __name__ == '__main__':
    main()
