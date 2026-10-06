# drift-detection

`detect-drift.sh` runs CloudFormation drift detection, and `drift_report.py` summarizes the result and holds a small diff function.

## Goal

Show how to find out that a deployed Orders stack no longer matches its template, and compare how each tool handles drift.

## Run it

```bash
python3 verify.py
python3 drift_report.py
```

Expected: `verify.py` prints `ok drift-detection: diff and report logic behave on simulated drift`. `drift_report.py` with no arguments prints its built-in sample: `MODIFIED  OrdersQueue /VisibilityTimeout` and `DELETED   OrdersTable`.

Not run end to end: `./detect-drift.sh orders-dev` needs AWS credentials and a deployed stack, so only the Python side ran. The script starts detection, polls until it finishes, writes `drift.json` and passes it to `drift_report.py`.

## What it proves

- `diff()` reports `/VisibilityTimeout` when a simulated console edit changes it from 30 to 120, and nothing when expected and actual match.
- A missing property is reported too: removing `RedrivePolicy` gives `/RedrivePolicy`.
- `report()` prints one line per resource with its status and drifted property paths.

| Tool | How drift is found | How it is fixed |
|---|---|---|
| CloudFormation | `detect-stack-drift` (on demand) | Update the stack, or edit the resource back |
| CDK | Same as CloudFormation (it deploys CFN) | `cdk deploy` |
| Pulumi | `pulumi refresh` or `preview --refresh` | `pulumi up` |
| Crossplane | Continuous reconciliation | Automatic |

## Trade-offs

- CloudFormation drift detection is on demand and does not cover every resource type.
- Continuous reconcilers fix drift unasked, which can overwrite an emergency manual fix.
- `diff()` is a simplified model of `PropertyDifferences`, not the real API output.

## When not to use it

- When all changes already go through a pipeline with locked-down console access.
- When your tool reconciles continuously, as Crossplane does.
