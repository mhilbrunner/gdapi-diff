#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import glob

from util.log import Log

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

class CLI:
    FILES_TO_CLOSE = []

    @staticmethod
    def add_file_argument(parser, f, *args, **kwargs):
        parser.add_argument(*args, **kwargs)
        CLI.add_file_to_close(f)

    @staticmethod
    def parse_args(arguments, doc, copyright, version):
        vname = str(sys.argv[0]) + " " + str(version)
        parser = argparse.ArgumentParser(
            description=doc,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=vname + copyright)

        parser.add_argument("-d", "--dumppath",
                            help="Dump folder path",
                            type=dir_path,
                            default=CLI.get_dump_path_default())

        CLI.add_file_argument(parser, "dumpfile1",
                              "-f1", "--dumpfile1", help="Input file #1",
                              type=argparse.FileType("r", encoding="utf8"))
        CLI.add_file_argument(parser, "dumpfile2",
                              "-f2", "--dumpfile2", help="Input file #2",
                              type=argparse.FileType("r", encoding="utf8"))

        CLI.add_file_argument(parser, "outfile",
                              "-o", "--outfile", help="Output file",
                              default=sys.stdout,
                              type=argparse.FileType("w", encoding="utf8"))

        parser.add_argument("-of", "--outputformat",
                            choices=["plain"],
                            default="plain")

        parser.add_argument("-e", "--edit", default=24,
                            help="Maximum edit distance allowed to use for " + \
                                 "comparisons. 0 to 100 (percent). " \
                                 "0 to disable. Requires Numpy.")

        parser.add_argument("-v", "--verbose", action="count",
                            default=int(Log.LOG_LEVEL),
                            help="Enable verbose logging")

        parser.add_argument("--version", action="version", version=vname)

        args = parser.parse_args(arguments)

        Log.set_level(args.verbose)
        Log.trace("Set log level to", args.verbose)

        if (args.dumpfile1 and not args.dumpfile2) or \
           (args.dumpfile2 and not args.dumpfile1):
            CLI.error(args,
              "If you specify a dump file, both files to compare must be given")

        if not args.dumpfile1:
            try:
                args = CLI.autoselect_dumpfiles(args)
            except Exception as e:
                CLI.error(args, "Error autoselecting dumpfiles: " + repr(e))

        try:
            import numpy
        except:
            Log.Warn("Numpy not found, edit distance checks will be disabled")
            args.edit = 0

        args.edit = int(args.edit)
        if args.edit < 0:
            args.edit = 0
        elif args.edit > 100:
            args.edit = 100

        return args

    @staticmethod
    def autoselect_dumpfiles(args):
        p = os.path.join(args.dumppath, "*")
        files = sorted(glob.iglob(p), reverse=True)
        filtered = []
        for f in files:
            if os.path.isdir(f):
                continue
            if not str(f).lower().endswith(".json"):
                continue
            filtered.append(f)

        if len(filtered) < 2:
            CLI.error(args, "Not enough dump files to autoselect in path", p)

        args.dumpfile1 = open(filtered[1], mode="r", encoding="utf8")
        args.dumpfile2 = open(filtered[0], mode="r", encoding="utf8")

        return args

    @staticmethod
    def get_dump_path_default():
        current_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(current_path, "..", "dumps"))

    @staticmethod
    def add_file_to_close(f):
        CLI.FILES_TO_CLOSE.append(f)

    @staticmethod
    def error(args, msg):
        CLI.cleanup(args)
        Log.error(msg)

    @staticmethod
    def cleanup(args):
        Log.trace("Cleaning up CLI parser")

        argsv = vars(args)
        for f in CLI.FILES_TO_CLOSE:
            try:
                if not f in argsv:
                    Log.warn("Unknown file to clean up", f)
                    continue

                if not argsv[f]:
                    continue

                if argsv[f] == sys.stdin or \
                   argsv[f] == sys.stdout or \
                   argsv[f] == sys.stderr:
                    Log.trace(f, "is STDIN/OUT/ERR, does not need to be closed")
                    continue

                if not argsv[f].closed:
                    Log.trace("Cleaning up", f)
                    argsv[f].close()
            except Exception as err:
                Log.warn("Error cleaning up file", f, repr(err))

        CLI.FILES_TO_CLOSE.clear()
