#!/usr/bin/env bash
# CloudFormation drift detection. Needs real AWS credentials: NOT run in this lab.
# Usage: ./detect-drift.sh [stack-name]
set -euo pipefail
STACK="${1:-orders-dev}"

ID=$(aws cloudformation detect-stack-drift --stack-name "$STACK" --query StackDriftDetectionId --output text)
until [ "$(aws cloudformation describe-stack-drift-detection-status --stack-drift-detection-id "$ID" \
  --query DetectionStatus --output text)" != DETECTION_IN_PROGRESS ]; do sleep 3; done

aws cloudformation describe-stack-resource-drifts --stack-name "$STACK" \
  --stack-resource-drift-status-filters MODIFIED DELETED \
  --query 'StackResourceDrifts[].[LogicalResourceId,StackResourceDriftStatus,PropertyDifferences[].PropertyPath]' \
  --output json > drift.json
python3 drift_report.py drift.json
