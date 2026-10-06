#!/usr/bin/env python3
"""Summarize drift: either `describe-stack-resource-drifts` output (a JSON file) or, with no args, a built-in sample.

The same expected-vs-actual diff idea underlies Pulumi refresh and Crossplane reconciliation.
"""
import json
import sys

SAMPLE = [["OrdersQueue", "MODIFIED", ["/VisibilityTimeout"]], ["OrdersTable", "DELETED", None]]


def diff(expected, actual, path=""):
    """Return property paths where actual differs from expected (CloudFormation's PropertyDifferences idea)."""
    out = []
    for k, v in expected.items():
        p = f"{path}/{k}"
        if k not in actual:
            out.append(p)
        elif isinstance(v, dict):
            out += diff(v, actual[k], p)
        elif v != actual[k]:
            out.append(p)
    return out


def report(rows):
    lines = []
    for logical, status, props in rows:
        lines.append(f"{status:9} {logical}" + (f" {', '.join(props)}" if props else ""))
    return lines


if __name__ == "__main__":
    rows = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else SAMPLE
    print("\n".join(report(rows)) or "no drift")
