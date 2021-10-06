#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import ceil

from util.log import Log

def compare(api1, api2, edit_distance):
    print("SINGLETONS")
    compare_names(api1["singletons"], api2["singletons"], edit_distance)
    print("CLASSES")
    compare_names(api1["classes"], api2["classes"], edit_distance)

def compare_names(l1, l2, edit_distance):
    # Compare l1 -> l2
    for name in l1:
        if name in l2:
            # Still exists, ignore
            continue

        # Try matching without underscore
        if name.startswith("_"):
            if name.lstrip("_") in l2:
                print(name + " -> " + name.lstrip("_"))
                continue

        # Try case-insensitive match
        found = False
        for other in l2:
            if name.lower() == other.lower():
                found = True
                print(name + " -> " + other)
                break
        if found:
            continue

        # Try edit distance match
        match = get_nearest_edit_distance(name, l2, edit_distance)
        if len(match) > 0:
            print(name + " -> " + match + "?")
            continue

        print(name + " -> ?")

    # Compare l2 -> l1
    for name in l2:
        if name in l1:
            # Still exists, ignore
            continue

        # Try case-insensitive match, ignore underscore
        found = False
        for other in l1:
            if name.lower() == other.lower().lstrip("_"):
                # Ignore, already found above
                found = True
                break
        if found:
            continue

        # Try edit distance match
        match = get_nearest_edit_distance(name, l1, edit_distance)
        if len(match) > 0:
            print(match + "? -> " + name)
            continue

        print("? -> " + name)

def get_nearest_edit_distance(token, tokens, edit_distance):
    if edit_distance < 1:
        return ""
    distances = {}
    for other in tokens:
        allowed_edit = ceil(float(edit_distance) *
                            float(len(token)/100.0))
        name_len_diff = max(len(token), len(other)) - \
        min(len(token), len(other))
        if name_len_diff > allowed_edit:
            continue
        d = levenshtein_distance(token, other)
        if ceil(d) > allowed_edit:
            continue
        distances[other] = d
    if len(distances) > 0:
        sort_orders = sorted(
            distances.items(), key=lambda x: x[1], reverse=True)
        return sort_orders[0][0]
    return ""

def levenshtein_distance(token1, token2):
    import numpy
    distance = numpy.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distance[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distance[0][t2] = t2

    a, b, c = 0, 0, 0

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distance[t1][t2] = distance[t1 - 1][t2 - 1]
            else:
                a = distance[t1][t2 - 1]
                b = distance[t1 - 1][t2]
                c = distance[t1 - 1][t2 - 1]

                if (a <= b and a <= c):
                    distance[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distance[t1][t2] = b + 1
                else:
                    distance[t1][t2] = c + 1

    return distance[len(token1)][len(token2)]
