#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple tool to compare Godot Engine API JSON dumps.
https://github.com/mhilbrunner/gdapi-diff

By default, it compares the last two dumpfiles in 'dumps/'
and writes API changes to STDOUT.
Dumpfiles to compare and the output file path can be set using CLI args.

To generate dump files, use the below commands with a Godot Engine executable:
godot --dump-extension-api (for Godot 4.0 and later)
godot --gdnative-generate-json-api api.kson (for Godot 3.x)

Requires Python 3.
Numpy is required for edit distance checks.
"""

COPYRIGHT = """
Licensed under the terms of the MIT license.

Godot Engine <https://godotengine.org>
Copyright (c) 2007-2021 Juan Linietsky, Ariel Manzur.
Copyright (c) 2014-2021 Godot Engine contributors.
"""

VERSION = "1.0"

import sys
import locale

from util.log import Log
from util.cli import CLI
from parseapi.parser import Parser
from diffapi.diff import compare

def main(arguments):
    locale.setlocale(locale.LC_ALL, '')
    args = CLI.parse_args(arguments, __doc__, COPYRIGHT, VERSION)

    try:
        p1 = Parser().parse(args.dumpfile1)
        p2 = Parser().parse(args.dumpfile2)

        compare(p1, p2, args.edit)
    except Exception as e:
        CLI.cleanup(args)
        raise e

    CLI.cleanup(args)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
