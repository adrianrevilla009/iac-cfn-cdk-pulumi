# crossplane

Three manifests, `xrd.yaml`, `composition.yaml` and `claim.yaml`, that offer the Orders stack as a Kubernetes API.

## Goal

Show the Orders stack as a Crossplane API: a CompositeResourceDefinition (`XOrderStack`, claim `OrderStack`), a composition that renders a queue and a table, and a claim that requests them.

## Run it

```bash
python3 verify.py
```

Expected: `ok crossplane: claim OrderStack fits XRD, composition has 2 resources`. It is offline and needs PyYAML.

Not run end to end: no cluster was used. On a cluster with Crossplane, the AWS SQS and DynamoDB providers and `function-patch-and-transform`, you would run `kubectl apply -f xrd.yaml -f composition.yaml` then `kubectl apply -f claim.yaml`. `kubectl delete -f claim.yaml` removes the cloud resources again.

## What it proves

- The XRD name, group and version match the composition's `compositeTypeRef` and the claim's `apiVersion` and `kind`.
- The claim only uses fields the XRD defines, its `env` value is in the `[dev, prod]` enum, and the required `env` is present.
- The composition is a pipeline with a `queue` and a `table` resource; `spec.region` from the composite is patched into each.

## Trade-offs

- Platform teams expose a small validated API and Kubernetes reconciles continuously, which also corrects drift.
- You run a control plane, provider packages are heavy, and compositions are harder to debug than a template.
- The composition has no dead-letter queue, and `env` is accepted but not patched into any resource, so it does not yet affect names.

## When not to use it

- Without an existing Kubernetes control plane.
- For one-off stacks, where CloudFormation, CDK or Pulumi are much lighter.
