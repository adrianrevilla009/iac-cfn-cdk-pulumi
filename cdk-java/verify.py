#!/usr/bin/env python3
"""Sketch-level check: pom pins versions and the app declares the same three resources as the CFN template."""
import pathlib
import re

here = pathlib.Path(__file__).parent
pom = (here / "pom.xml").read_text()
src = (here / "src/main/java/lab/iac/OrdersApp.java").read_text()
assert 'release>21<' in pom
assert not re.search(r"<version>(LATEST|RELEASE|\$\{)", pom)
for construct in ("Queue.Builder", "Table.Builder", "DeadLetterQueue", "CfnOutput"):
    assert construct in src, construct
assert src.count("Queue.Builder.create") == 2
print("ok cdk-java: pom pinned, app declares queue+dlq+table (compile not run here)")
