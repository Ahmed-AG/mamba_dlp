import boto3
import json

#Assume Role on a certain AWS account
def assume_role(aws_account,role):
	sts_client = boto3.client('sts')
	assumedRoleObject = sts_client.assume_role(
		RoleArn="arn:aws:iam::" + aws_account + ":role/" + role,
		RoleSessionName="Session1"
		)
	return assumedRoleObject

def input_radio_choice(question , choices):
	while (1):
		choice = input(question)
		if (choice in choices):
			return choice
		else:
			print("Input Error! Please choose from: \n" + str(choices))
	return

def load_conf(conf_file_location):
		conf_file= open(conf_file_location,'r')
		conf=json.load(conf_file)

		return conf

def save_config_to_file(config , file):

	with open(file, 'w', encoding='utf-8') as f:
		json.dump(config, f, ensure_ascii=False, indent=2)
	print("conf_file generated:")
	print(json.dumps(config , sort_keys=True , indent=2))
	print("saved to: " + file)

	return
