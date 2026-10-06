#!/usr/bin/env python3
"""Offline check: the claim matches the XRD, and the composition targets the XRD's composite kind."""
import pathlib

import yaml

here = pathlib.Path(__file__).parent
xrd, comp, claim = (yaml.safe_load((here / f).read_text()) for f in ("xrd.yaml", "composition.yaml", "claim.yaml"))

group = xrd["spec"]["group"]
version = xrd["spec"]["versions"][0]
assert xrd["metadata"]["name"] == f"{xrd['spec']['names']['plural']}.{group}"
ref = comp["spec"]["compositeTypeRef"]
assert ref == {"apiVersion": f"{group}/{version['name']}", "kind": xrd["spec"]["names"]["kind"]}
assert claim["apiVersion"] == ref["apiVersion"] and claim["kind"] == xrd["spec"]["claimNames"]["kind"]

schema = version["schema"]["openAPIV3Schema"]["properties"]["spec"]
assert set(claim["spec"]) <= set(schema["properties"]), "claim uses fields the XRD does not define"
assert claim["spec"]["env"] in schema["properties"]["env"]["enum"]
assert set(schema["required"]) <= set(claim["spec"])

resources = comp["spec"]["pipeline"][0]["input"]["resources"]
assert {r["name"] for r in resources} == {"queue", "table"}
print(f"ok crossplane: claim {claim['kind']} fits XRD, composition has {len(resources)} resources")
