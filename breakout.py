#!/usr/bin/env python
from __future__ import absolute_import, division, unicode_literals

import argparse
import locale


__version__ = '0.1'


def main():
    """Entry point when called on the command-line.
    """
    # Locale
    locale.setlocale(locale.LC_ALL, '')

    parser = argparse.ArgumentParser(
        description="breakout - drop to debugger when given output is written")
    parser.add_argument('--regex', '-r', nargs=argparse.ZERO_OR_MORE,
                        help="Regular expression to break on")
    parser.add_argument('--text', '-t', nargs=argparse.ZERO_OR_MORE,
                        help="Text output to break on")
    parser.add_argument('--stdout', action='store_true', default=False,
                        help="Only watch stdout")
    parser.add_argument('--stderr', action='store_true', defaut=False,
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
        setup_watch(text=args.text, regex=args.regex,
                    stdout=args.stdout, stderr=args.stderr)
    else:
        setup_watch(text=args.text, regex=args.regex)

    if args.module:
        execute_module(args.module)
    else:
        execute_script(args.cmdline)


if __name__ == '__main__':
    main()
