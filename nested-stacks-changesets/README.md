# nested-stacks-changesets

A parent template, two child templates (queues, table) and `changeset.sh`, which previews changes before applying them.

## Goal

Split the Orders stack into a parent and two nested child stacks, and show the change-set flow that previews every change before it is executed.

## Run it

```bash
python3 verify.py
```

Expected: `ok nested-stacks-changesets: 2 children wired`. It is offline and needs PyYAML.

Not run end to end: `BUCKET=my-bucket ./changeset.sh orders-nested` needs AWS credentials and an S3 bucket you own, so it was never executed. It would run `package`, `create-change-set`, wait, and `describe-change-set`, then print the execute and delete-stack commands. Cost should be near zero.

## What it proves

- `parent.yaml` declares two `AWS::CloudFormation::Stack` resources, `Queues` and `Table`, pointing at `child-queues.yaml` and `child-table.yaml`.
- Every parameter the parent passes (`Env`) exists in the child, and the parent outputs `QueueUrl` and `TableName` reference real nested stacks via `GetAtt`.
- `changeset.sh` picks `CREATE` or `UPDATE` by checking whether the stack exists, then lists action, logical id and replacement per change.

## Trade-offs

- Nested stacks keep templates small and reusable, but need an S3 bucket for the child templates and deploy more slowly.
- Change sets show replacements before they happen; nested ones are harder to read than flat ones.
- The children are simpler than `cloudformation-stacks/orders-stack.yaml`: no visibility timeout, retention period or `prod` retain policy.

## When not to use it

- For a stack this small, where a single template is simpler.
- For reuse across accounts, where modules or a CDK construct fit better.
