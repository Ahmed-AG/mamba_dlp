
import sys
import boto3
import time
import json
import argparse
import logging
import os.path
import botocore
import os

import utils

def run_configure(default_conf_file):
	print("*** mamba_dlp configuration wizard")
	#Generate conf file
	default_conf_file_exists = os.path.exists(default_conf_file)
	if (default_conf_file_exists):
		default_conf_file_content = utils.load_conf(default_conf_file)
	else:
		default_conf_file_content = ""

	print(f"Checking default conf file {default_conf_file}: {default_conf_file_exists}")
	print(json.dumps(default_conf_file_content , indent =2))

	if (utils.input_radio_choice("Generate conf file? (y/n): ",["y","n"]) == "y"):
		conf_file_json = generate_conf_file(default_conf_file)
		config = conf_file_json
		utils.save_config_to_file(conf_file_json , default_conf_file)
	else:
		if (os.path.exists(default_conf_file)):
			config = utils.load_conf(default_conf_file)
		else:
			print("Default conf file \"" + default_conf_file + "\" Not found!")
			exit()
	#deloy Dynamotable
	
	table_name = config['global_conf']['dynamo_table']
	print(f"Checking Dynamo table: {table_name}: {check_dynamo_table(table_name)}")
	deploy_dynamo_table(table_name)
	
	#configure realtime
	if (utils.input_radio_choice("Configure mamba_dlp realtime? (y/n): ",["y","n"]) == "y"):
		for aws_account in config['global_conf']['aws_accounts']:
			cfn_bucket = input("Enter bucket name to be used for Cloudformation template: ")
			function_arn = deploy_realtime_function(aws_account , cfn_bucket , table_name)
			deploy_realtime(aws_account , function_arn)

def check_dynamo_table(table_name):

	return False

def deploy_dynamo_table(table_name):
	if (utils.input_radio_choice(f"Deploy Dyamo table {table_name}? (y/n): ",["y","n"]) == "y"):
		os.system(f"aws cloudformation deploy \
			--region us-east-1 \
			--template-file deploy/deploy_dynamo_table.yaml \
			--stack-name mamba-db-stack \
			--parameter-overrides \
			DynamoTable={table_name} \
			")


def generate_conf_file(default_conf_file):
	config ={'global_conf':{}}

	print("*** mamba_dlp generate conf file: " + default_conf_file)
	config['global_conf']['aws_accounts']=[]
	config['global_conf']['aws_role']=""

	config['global_conf']['aws_accounts'] =[ input("Enter aws_account :") ]
	config['global_conf']['dynamo_table'] = input("Dynamo table name? ")
	#Configure actions
	config['global_conf']['actions'] = []

	#The loop is a for future additional actions
	#configure tagging 
	while(1):
		tagging = {'tagging':[]}
		supported_data_types =["payment_card" , "email_address"]
		print("Configuring Actions")
		tagging_enabled = utils.input_radio_choice("Enable tagging of resources upon detection of sensitive data? (true/false): ",["true", "false"])
		if tagging_enabled == "false":
			break
		for data_type in supported_data_types:
			enabled = utils.input_radio_choice("Data Type: \"" + data_type + "\" : Enable tagging ? (true/false): ",["true", "false"])
			tag_set_key = input("Data Type: \"" + data_type + "\" : Enter tag_set Key: ")
			tag_set_value = input("Data Type: \"" + data_type + "\" : Enter tag_set Value: ")

			tagging['tagging'].append({'data_type' : data_type,
							'enabled' : enabled,
                            "tag_set" : 
							 	{
							 		"Key": tag_set_key, 
							 		"Value": tag_set_value 
							 	}
					})
			
		break
	config['global_conf']['actions'].append(tagging)
	return config

def deploy_realtime_function(aws_account , cfn_bucket , dynamo_table):
	print("*** Running deployment script: deploy/deploy_realtime.sh")
	os.system(f"sh deploy/deploy_realtime.sh {aws_account} {cfn_bucket} {dynamo_table}")

	client = boto3.client('cloudformation')
	response = client.list_exports()
	for exports in response['Exports']:
		if exports['Name'] == 'MambaLambdaArn':
			mamba_function_arn = exports['Value']
	return mamba_function_arn
			
def deploy_realtime(aws_account , function_arn):
	client = boto3.client('s3')
	buckets=client.list_buckets()

	for bucket in buckets['Buckets']:
		bucket_arn = "arn:aws:s3:::" + bucket['Name']
		print("*** Configuring: " + bucket_arn)
		
		print(add_lambda_permission(function_arn , bucket['Name'] ))
		print(add_bucket_notification(function_arn ,bucket['Name']))

	return

def add_lambda_permission(function_arn , bucket_name ):
	try:
		bucket_arn = "arn:aws:s3:::" + bucket_name
		statement_id = "mamba_dlp_" + bucket_name

		client = boto3.client('lambda')
		add_permission = client.add_permission(
				FunctionName=function_arn,
				StatementId = statement_id,
				Action='lambda:invokeFunction',
				Principal='s3.amazonaws.com',
				SourceArn = bucket_arn
				)
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "InvalidArgument":
			return "Error: " + e.response['Error']['Message']
		elif e.response['Error']['Code'] == "ResourceConflictException":
			return "Warning: Lambda policy statement ID: " + statement_id + " already exists"
		else:
			return e.response
	
	return "lambda_permission added!"

def add_bucket_notification(function_arn , bucket_name):
	try:
		s3 = boto3.resource('s3')
		bucket_notification = s3.BucketNotification(bucket_name)
		response = bucket_notification.put(NotificationConfiguration={'LambdaFunctionConfigurations': [
				{
			'LambdaFunctionArn': function_arn,
			'Events': [
			's3:ObjectCreated:*'
			],
			'Id':'mamba_dlp_realtime'
			},
			]})
		
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "AccessDenied":
			return "Error: " + e.response['Error']['Message']
		elif e.response['Error']['Code'] == "InvalidArgument":
			return "Error: " + e.response['Error']['Message']
		elif e.response['Error']['Message'] == "The statement id (string) provided already exists. Please provide a new statement id, or remove the existing statement.":
			return "Warning: Lambda policy already exists"
		else:
			return e.response
	return "bucket_notification added!"
