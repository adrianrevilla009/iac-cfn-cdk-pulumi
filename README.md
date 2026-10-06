# iac-cfn-cdk-pulumi

The same small Orders stack (queue, dead-letter queue, DynamoDB table) written in CloudFormation, CDK, Pulumi and Crossplane, so you can compare how each tool describes, previews and corrects infrastructure.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`cloudformation-stacks`](./cloudformation-stacks) | One CloudFormation template with a parameter, a condition and outputs | `python3 verify.py` |
| [`nested-stacks-changesets`](./nested-stacks-changesets) | Parent stack with two nested child stacks and a change-set preview script | `python3 verify.py` |
| [`cdk-java`](./cdk-java) | The same stack as a CDK app in Java | `python3 verify.py` |
| [`pulumi-java`](./pulumi-java) | The same stack as a Pulumi program in Java | `python3 verify.py` |
| [`crossplane`](./crossplane) | A Crossplane XRD, composition and claim for the stack | `python3 verify.py` |
| [`drift-detection`](./drift-detection) | CloudFormation drift detection script and a tested diff/report helper | `python3 verify.py` |

Each `verify.py` is an offline check; nothing in this repo talks to a cloud account. Deploy and destroy commands are written in the folder READMEs but were not run.

| | CloudFormation | CDK (Java) | Pulumi (Java) | Crossplane |
|---|---|---|---|---|
| Language | YAML | Java, synthesizes CloudFormation | Java | YAML (Kubernetes CRDs) |
| State | Managed by AWS | Managed by AWS (CloudFormation) | Backend you pick | Kubernetes etcd |
| Preview | Change sets | `cdk diff` | `pulumi preview` | None (reconciles) |
| Drift | On demand | On demand (CloudFormation) | `pulumi refresh` | Continuous |
| Needs | AWS CLI | Node + CDK CLI | Pulumi CLI + backend | A Kubernetes cluster |

## Prerequisites

- Python 3 with PyYAML (all `verify.py` scripts).
- To go beyond the offline checks: AWS CLI, Java 21 and Maven, Node (for `aws-cdk@2.170.0`), Pulumi CLI, and a Kubernetes cluster with Crossplane.

## How to read it

Start with `cloudformation-stacks`, since the CDK and Pulumi programs mirror it resource by resource. Then read `cdk-java` and `pulumi-java` side by side, and finish with `crossplane` and `drift-detection`.
