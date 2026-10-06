# cdk-java

A CDK app in Java (`OrdersApp.java`) that declares the Orders queue, dead-letter queue and table.

## Goal

Express the shared Orders stack with the AWS CDK in Java, for a side-by-side comparison with the raw CloudFormation template.

## Run it

```bash
python3 verify.py
```

Expected: `ok cdk-java: pom pinned, app declares queue+dlq+table (compile not run here)`.

Not run end to end: the Java code was never compiled and `cdk synth` was never executed, because the CDK libraries and CLI were not installed here. With Maven, Java 21 and Node available, `npx aws-cdk@2.170.0 synth` would print CloudFormation without calling AWS; `deploy` and `destroy` need a bootstrapped account.

## What it proves

- `pom.xml` pins Java 21, `aws-cdk-lib` 2.170.0, `constructs` 10.4.2 and the exec plugin 3.5.0, with no ranges; `cdk.json` runs the app with `mvn -q compile exec:java`.
- `OrdersApp.java` creates two `Queue` constructs and one `Table`; the dead-letter queue is wired in a single `deadLetterQueue(...)` call with `maxReceiveCount(5)`.
- The static check confirms those constructs and the two `CfnOutput` values are present in the source.

## Trade-offs

- A real language gives completion and reusable constructs, but adds a Node CLI dependency and a bootstrap step per account.
- The generated template is harder to review than hand-written YAML.
- This app hardcodes the `dev` names and `RemovalPolicy.DESTROY`; it has no `Env` parameter or `prod` retain like the CloudFormation version.

## When not to use it

- For tiny, stable stacks, or teams without a JVM toolchain; plain CloudFormation is simpler.
