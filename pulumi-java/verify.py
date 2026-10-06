#!/usr/bin/env python3
"""Sketch-level check: Pulumi project files exist, versions are pinned, the program declares the Orders resources."""
import pathlib
import re

import yaml

here = pathlib.Path(__file__).parent
meta = yaml.safe_load((here / "Pulumi.yaml").read_text())
assert meta["runtime"]["name"] == "java"
pom = (here / "pom.xml").read_text()
src = (here / "src/main/java/lab/iac/App.java").read_text()
assert 'release>21<' in pom
assert not re.search(r"<version>(LATEST|RELEASE|\$\{)", pom)
assert src.count("new Queue(") == 2 and "new Table(" in src and "redrivePolicy" in src
print("ok pulumi-java: project pinned, program declares queue+dlq+table (compile not run here)")
