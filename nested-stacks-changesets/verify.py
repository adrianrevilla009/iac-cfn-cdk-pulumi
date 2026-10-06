#!/usr/bin/env python3
"""Offline check: parent nested stacks reference child files that exist and whose parameters line up."""
import pathlib
import yaml

here = pathlib.Path(__file__).parent


def intrinsic(loader, suffix, node):
    if isinstance(node, yaml.ScalarNode):
        return {suffix: loader.construct_scalar(node)}
    if isinstance(node, yaml.SequenceNode):
        return {suffix: loader.construct_sequence(node, deep=True)}
    return {suffix: loader.construct_mapping(node, deep=True)}


class Loader(yaml.SafeLoader):
    pass


Loader.add_multi_constructor("!", intrinsic)
load = lambda n: yaml.load((here / n).read_text(), Loader)

parent = load("parent.yaml")
stacks = {k: v for k, v in parent["Resources"].items() if v["Type"] == "AWS::CloudFormation::Stack"}
assert len(stacks) == 2
for name, s in stacks.items():
    url = s["Properties"]["TemplateURL"]["Sub"]
    child_file = url.rsplit("/", 1)[1]
    child = load(child_file)
    missing = set(s["Properties"]["Parameters"]) - set(child["Parameters"])
    assert not missing, f"{name}: child lacks parameters {missing}"
for ref in (v["Value"]["GetAtt"] for v in parent["Outputs"].values()):
    logical, _, out = ref.split(".", 2)
    assert logical in stacks, ref
print(f"ok nested-stacks-changesets: {len(stacks)} children wired")
