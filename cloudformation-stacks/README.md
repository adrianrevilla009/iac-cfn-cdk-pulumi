# cloudformation-stacks

A single CloudFormation template, `orders-stack.yaml`, with an Orders queue, a dead-letter queue and a DynamoDB table.

## Goal

Define the shared Orders stack as a plain CloudFormation template with a parameter, a condition and outputs. The sibling folders rebuild the same stack in CDK and Pulumi.

## Run it

```bash
python3 verify.py
```

Expected: `ok .../orders-stack.yaml: 3 resources`. It needs PyYAML and makes no AWS calls.

Not run end to end: a real deploy needs an AWS account. The commands would be `aws cloudformation deploy --template-file orders-stack.yaml --stack-name orders-dev` and, to clean up, `aws cloudformation delete-stack --stack-name orders-dev`. Cost should be near zero (SQS and pay-per-request DynamoDB).

## What it proves

- `verify.py` loads the template (with intrinsic short forms like `!Ref` and `!Sub`) and checks the format version, that it has `Parameters` and `Outputs`, and that the only resource types are `AWS::SQS::Queue` and `AWS::DynamoDB::Table`.
- The `Env` parameter (`dev` or `prod`) names every resource, and `OrdersQueue` redrives to `OrdersDlq` after 5 receives.
- The `IsProd` condition sets the table's `DeletionPolicy` to `Retain` for `prod` and `Delete` otherwise.

## Trade-offs

- Declarative YAML is explicit and has no runtime, but offers no loops or types beyond intrinsic functions.
- The check is structural only; it does not run `cfn-lint` or ask CloudFormation to validate the template.
- Fixed queue names make a second copy of the stack in the same account and region clash unless `Env` differs.

## When not to use it

- When you need real logic, shared abstractions or several clouds; CDK or Pulumi fit better.
