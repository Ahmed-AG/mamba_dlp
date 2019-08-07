import boto3

#Assume Role on a certain AWS account
def assume_role(aws_account,role):
	sts_client = boto3.client('sts')
	assumedRoleObject = sts_client.assume_role(
		RoleArn="arn:aws:iam::" + aws_account + ":role/" + role,
		RoleSessionName="Session1"
		)
	return assumedRoleObject
