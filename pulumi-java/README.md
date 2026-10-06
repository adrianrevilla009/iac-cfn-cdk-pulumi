# pulumi-java

A Pulumi program in Java (`App.java`) with a `Pulumi.yaml` project file and a `pom.xml`, declaring the Orders queue, dead-letter queue and table.

## Goal

Express the shared Orders stack with Pulumi in Java, to compare its state model and workflow with CloudFormation and CDK.

## Run it

```bash
python3 verify.py
```

Expected: `ok pulumi-java: project pinned, program declares queue+dlq+table (compile not run here)`.

Not run end to end: the Java code was never compiled and Pulumi was never run, because the Pulumi CLI and dependencies were not installed here. With them, `mvn -q package` then `pulumi login --local` and `pulumi preview --stack dev` would show the plan; `pulumi up` and `pulumi destroy` need a real AWS account.

## What it proves

- `Pulumi.yaml` selects the Java runtime and points at `target/pulumi-java-1.0.0.jar`; `verify.py` checks the runtime name, Java 21 in `pom.xml`, and that no version is a range.
- `App.java` declares two `Queue` resources and one `Table`, and exports `queueUrl` and `tableName`.
- The redrive policy is a JSON string built from the dead-letter queue's ARN with `applyValue`, because the ARN is only known at deploy time.

## Trade-offs

- Pulumi gives real state management and previews across clouds, but you must run a state backend.
- The AWS provider can lag new CloudFormation features, and Java outputs need `applyValue`, which is more verbose than CDK.
- The names are hardcoded to `dev`; there is no environment config as in `cloudformation-stacks`.

## When not to use it

- When the team is AWS-only and content with CloudFormation or CDK.
- When you cannot host or trust a state backend.
