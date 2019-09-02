#!/bin/bash
aws_account=$1
cfn_bucket=$2
dynamo_table=$3
zip_file="lambda_code.zip"
code_dir="code"

cd $code_dir
chmod +rw *
zip -r $zip_file *

aws s3 cp $zip_file s3://$cfn_bucket/$zip_file
rm $zip_file

aws cloudformation deploy --capabilities CAPABILITY_NAMED_IAM CAPABILITY_IAM \
	--region us-east-1 \
	--template-file ../deploy/deploy_realtime_lambda.yaml \
	--stack-name mamba-realtime-stack \
	--parameter-overrides \
	LambdaS3Bucket=$cfn_bucket \
	LambdaS3Object=$zip_file \
	DynamoTable=$dynamo_table \

	
