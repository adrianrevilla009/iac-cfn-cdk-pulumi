#!/usr/bin/env bash
# Review-before-apply flow for the nested stack. Needs real AWS credentials: NOT run in this lab.
# Usage: BUCKET=my-bucket ./changeset.sh [stack-name]
set -euo pipefail
STACK="${1:-orders-nested}"
: "${BUCKET:?set BUCKET to an S3 bucket you own}"

aws cloudformation package --template-file parent.yaml --s3-bucket "$BUCKET" --output-template-file packaged.yaml
aws cloudformation create-change-set --stack-name "$STACK" --change-set-name preview \
  --template-body file://packaged.yaml --capabilities CAPABILITY_AUTO_EXPAND \
  --parameters ParameterKey=TemplatesBucket,ParameterValue="$BUCKET" \
  --change-set-type "$(aws cloudformation describe-stacks --stack-name "$STACK" >/dev/null 2>&1 && echo UPDATE || echo CREATE)"
aws cloudformation wait change-set-create-complete --stack-name "$STACK" --change-set-name preview
aws cloudformation describe-change-set --stack-name "$STACK" --change-set-name preview \
  --query 'Changes[].ResourceChange.[Action,LogicalResourceId,Replacement]' --output table
echo "Apply:   aws cloudformation execute-change-set --stack-name $STACK --change-set-name preview"
echo "Destroy: aws cloudformation delete-stack --stack-name $STACK"
