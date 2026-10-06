#!/usr/bin/env python3
"""Offline structural check of a CloudFormation template (no AWS calls)."""
import os
import sys
import yaml


class Loader(yaml.SafeLoader):
    pass


# Treat intrinsic short forms (!Ref, !Sub, ...) as plain values.
def intrinsic(loader, suffix, node):
    if isinstance(node, yaml.ScalarNode):
        return {suffix: loader.construct_scalar(node)}
    if isinstance(node, yaml.SequenceNode):
        return {suffix: loader.construct_sequence(node, deep=True)}
    return {suffix: loader.construct_mapping(node, deep=True)}


Loader.add_multi_constructor("!", intrinsic)


def main(path):
    t = yaml.load(open(path), Loader)
    res = t["Resources"]
    assert t["AWSTemplateFormatVersion"] == "2010-09-09"
    for name, r in res.items():
        assert r["Type"].startswith("AWS::"), name
    assert {r["Type"] for r in res.values()} == {"AWS::SQS::Queue", "AWS::DynamoDB::Table"}
    assert "Outputs" in t and "Parameters" in t
    print(f"ok {path}: {len(res)} resources")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "orders-stack.yaml"))
