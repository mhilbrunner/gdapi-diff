#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from util.log import Log

def construct_api_dict():
    d = {}
    d["version_major"] = None
    d["version_minor"] = None
    d["version_patch"] = None
    d["version_known"] = False
    d["singletons"] = {}
    d["classes"] = {}
    return d

class Parser:
    def parse(self, f):
        Log.info("Parsing", f.name)
        j = json.load(f)

        # Detect which parser to use for Godot Engine version/API dump
        if not "header" in j:
            # Godot 3?
            Log.trace("Using Godot 3 API dump parser")
            return ParserGD3().parse(j)
        else:
            if not "version_major" in j["header"]:
                raise Exception("Missing version_major in API dump header")
            else:
                if j["header"]["version_major"] == 4:
                    # Godot 4
                    Log.trace("Using Godot 4 API dump parser")
                    return ParserGD4().parse(j)
                else:
                    # Future version
                    raise Exception("Unsupported version_major in API dump: " +
                                    str(j["header"]["version_major"]))


class ParserGD3:
    def parse(self, data):
        result = construct_api_dict()
        result["version_major"] = 3

        for x in data:
            if "singleton" in x and x["singleton"]:
                result["singletons"][x["name"]] = True
            else:
                result["classes"][x["name"]] = True

        return result

class ParserGD4:
    def parse(self, data):
        result = construct_api_dict()
        result["version_major"] = data["header"]["version_major"]
        result["version_minor"] = data["header"]["version_minor"]
        result["version_patch"] = data["header"]["version_patch"]
        result["version_known"] = True

        for s in data["singletons"]:
            result["singletons"][s["name"]] = True

        for c in data["classes"]:
            result["classes"][c["name"]] = True

        return result
