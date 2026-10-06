#!/usr/bin/env python3
"""Offline check of the drift diff and report logic using a simulated console edit."""
from drift_report import SAMPLE, diff, report

expected = {"VisibilityTimeout": 30, "RedrivePolicy": {"maxReceiveCount": 5}}
actual = {"VisibilityTimeout": 120, "RedrivePolicy": {"maxReceiveCount": 5}}  # someone edited it by hand
assert diff(expected, actual) == ["/VisibilityTimeout"]
assert diff(expected, expected) == []
assert diff(expected, {"VisibilityTimeout": 30}) == ["/RedrivePolicy"]
lines = report(SAMPLE)
assert lines[0].startswith("MODIFIED") and "/VisibilityTimeout" in lines[0] and lines[1].startswith("DELETED")
print("ok drift-detection: diff and report logic behave on simulated drift")
