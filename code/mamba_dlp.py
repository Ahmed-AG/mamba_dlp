#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import sys
import boto3
import time
import json
import argparse
import logging


import data_source
import data_finder
import aws
import state_object
import actions

def lambda_handler(event, context):
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)

	conf_file = "conf/mamba_dlp.conf"
	config = load_conf(conf_file)

	#Obtain local account ID
	client = boto3.client("sts")
	aws_account = client.get_caller_identity()["Account"]

	#Read event
	for record in event['Records']:
		bucket=record['s3']['bucket']['name']
		key=record['s3']['object']['key']
		object_id=aws_account + ":" + bucket + ":" + key
		#build object to scan
		object_to_scan={'objects':[]}
		object_to_scan['objects'].append({'object_id' : object_id,
                         'object_type' : 's3',
                         'aws_account': aws_account,
                         'bucket': bucket, 
                         'key': key
                        }
                        )
                
	print(json.dumps(object_to_scan , sort_keys=True , indent=2))
	#run scan
	state = state_object.sensitive_data(config['global_conf']['dynamo_table'])
	sesitive_data = scan_single_object(config , state , json.dumps(object_to_scan))
	

	action = actions.action(config)
	action_response = action.initiate(sesitive_data)
	

	print("Sensitive Data Found:")
	print(json.dumps(sesitive_data , sort_keys=True , indent=2))

	return

def display_banner():

    print("                           _                _ _       ")
    print("                          | |              | | |      ")
    print(" _ __ ___   __ _ _ __ ___ | |__   __ _   __| | |_ __  ")
    print("| '_ ` _ \ / _` | '_ ` _ \| '_ \ / _` | / _` | | '_ \ ")
    print("| | | | | | (_| | | | | | | |_) | (_| || (_| | | |_) |")
    print("|_| |_| |_|\__,_|_| |_| |_|_.__/ \__,_| \__,_|_| .__/ ")
    print("                                    ______     | |    ")
    print("                                   |______|    |_|    ")

    return

def print_usage():
	print ("Usage: ")
	print ("mamba_dlp.py --run full_scan")
	print ("mamba_dlp.py --run scan_object --object <Json Object>")
	print ("mamba_dlp.py --run scan_object --aws_account <aws account> --bucket <bucket name> --key <key>")
	return

def load_conf(conf_file_location):
		conf_file= open(conf_file_location,'r')
		conf=json.load(conf_file)

		return conf

def full_scan(config , state ):

	finder = data_finder.finder(config['global_conf']['dynamo_table'])
	s3 = data_source.s3(config['global_conf']['aws_accounts'] , config['global_conf']['aws_role'])
	s3.objects = s3.find_objects()
	sesitive_data = finder.scan_objects(s3)

	#Actions
	action = actions.action(config)
	action_response = action.initiate(sesitive_data)
	

	return sesitive_data

def scan_single_object(config , state ,  object):
	finder = data_finder.finder(config['global_conf']['dynamo_table'])
	s3 = data_source.s3(config['global_conf']['aws_accounts'] , config['global_conf']['aws_role'])
	s3.objects = json.loads(object)
	sesitive_data = finder.scan_objects(s3)
	
	#Actions
	action = actions.action(config)
	action_response = action.initiate(sesitive_data)
	#print(action_response)


	return sesitive_data

def main():

	####### Main starts here ####### 

	display_banner()

	#process arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--run', required=1)
	parser.add_argument('--config')
	parser.add_argument('--object')
	parser.add_argument('--key')
	parser.add_argument('--bucket')
	parser.add_argument('--aws_account')

	args = parser.parse_args()

	#load configurations
	if args.config == None:
		conf_file = "code/conf/mamba_dlp.conf"
	else:
		conf_file = args.config

	config = load_conf(conf_file)

	#Start logic
	if args.run == "full_scan":
		state = state_object.sensitive_data(config['global_conf']['dynamo_table'])
		scan_result = full_scan(config , state )
		print("Sensitive Data Found:")
		print(json.dumps(scan_result , sort_keys=True , indent=2))

	elif args.run == "scan_object":
		if args.object != None:
			#scan single object
			state = state_object.sensitive_data(config['global_conf']['dynamo_table'])
			scan_result = scan_single_object(config , state , args.object)
			print("Sensitive Data Found:")
			print(json.dumps(scan_result , sort_keys=True , indent=2))
		elif args.bucket != None and args.key != None and args.aws_account != None:
			#Build the object from arguments
			object_id = args.aws_account + ":" + args.bucket + ":" + args.key
			object = {"objects":[ {
			"object_id" : object_id,
			"object_type" : "s3",
			"aws_account" : args.aws_account,
			"bucket" : args.bucket,
			"key" : args.key
			}]}

			state = state_object.sensitive_data(config['global_conf']['dynamo_table'])
			scan_result = scan_single_object(config , state , json.dumps(object))
			print("Sensitive Data Found:")
			print(json.dumps(scan_result , sort_keys=True , indent=2))

		else:
			print_usage()
			exit()

	elif args.run == "deploy_real_time_dlp":
		# Deploy Cloud formation template install realtime DLP
		print("Deploy Cloud formation template install realtime DLP")
	else:
		print_usage()
	    	    

if sys.argv[0] != "/var/runtime/awslambda/bootstrap.py":
	main()

