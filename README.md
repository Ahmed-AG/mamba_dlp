
BETA - mamba_dlp
================

Mamba_dlp is a tool for searching for sensitive data in cloud infrastructures.

Current features of Mamba_dlp:

- **Search for sensitive data**: using customizable regex, mamba_dlp scans through data sources and reports any sensitive data. mamba_dlp can run full scans or can scan a single object 
- **Search for sensitive data in:**
	-S3 Buckets
-**Search for the following data types:**
	-Credit Cards
	-Emails
	-Any custom regex
-**Output:**
	-Json object
	-Dynamo table

Before you begin 
----------------
- **Configuration:**
	If no configuration file was provided manually, mambda_dlp will check for the default configuration file "code/conf/mamba_dlp.conf".

	If the file does not exist you will be prompted with the option to create one. If you chose "Yes" a quick wizard will build one for you.

	Alternatively. you can manually create a new config file at anytime by using  "--run configure"

	```sh
	$python3 code/mamba_dlp.py --run configure
	                           _                _ _       
	                          | |              | | |      
	 _ __ ___   __ _ _ __ ___ | |__   __ _   __| | |_ __  
	| '_ ` _ \ / _` | '_ ` _ \| '_ \ / _` | / _` | | '_ \ 
	| | | | | | (_| | | | | | | |_) | (_| || (_| | | |_) |
	|_| |_| |_|\__,_|_| |_| |_|_.__/ \__,_| \__,_|_| .__/ 
	                                    ______     | |    
	                                   |______|    |_|    
	mamba_dlp configure:
	Building conf/mamba_dlp.conf:
	Enter aws_account ************
	Dynamo table name? sensitive_data
	Configuring Actions
	Enable tagging of resources upon detection of sensitive data? (true/false): true
	Data Type: "payment_card" : Enable tagging ? (true/false): true
	Data Type: "payment_card" : Enter tag_set Key: pci_sensitive_data
	Data Type: "payment_card" : Enter tag_set Value: true
	Data Type: "email_address" : Enable tagging ? (true/false): true
	Data Type: "email_address" : Enter tag_set Key: email_address
	Data Type: "email_address" : Enter tag_set Value: true
	conf_file generated:
	{
	  "global_conf": {
	    "actions": [
	      {
	        "tagging": [
	          {
	            "data_type": "payment_card",
	            "enabled": "true",
	            "tag_set": {
	              "Key": "pci_sensitive_data",
	              "Value": "true"
	            }
	          },
	          {
	            "data_type": "email_address",
	            "enabled": "true",
	            "tag_set": {
	              "Key": "email_address",
	              "Value": "true"
	            }
	          }
	        ]
	      }
	    ],
	    "aws_accounts": [
	      "************"
	    ],
	    "aws_role": "",
	    "dynamo_table": "sensitive_data"
	  }
	}
	saved to: code/conf/mamba_dlp.conf
	$
	```


Getting Started 
----------------
- **Scan all files in all buckets:**
	```sh
	$python3 code/mamba_dlp.py --run full_scan
	```
- **Scan a single file:**

	To scan a single file provide the AWS account number, the bucket name and the key name:

	```sh
	 python3 code/mamba_dlp.py --run scan_object --bucket <bucket name> --key <key name> --aws_account <aws account name>
	 ```

	Or manually construct the object json descriptor:

	```sh
	python3 code/mamba_dlp.py --run scan_object --object \
		"{\"objects\" : [{\"object_id\" : \"<AWS_ACCOUNT>:<BUCKET:KEY\",\
		 \"object_type\" : \"s3\",\
		 \"aws_account\": \"<AWS_ACCOUNT>\",\
		 \"bucket\": \"<BUCKET>\", \"key\": \"<KEY>\" }]}"
	```

- **Scan in real time:** to configure mamba_dlp to scan files in as they are updated or uploaded to a bucket:

	- Clone this repo
	- Create a Dynamo table that has the following:
		- Primary partition key : object_id (String)
		- Primary sort key : location (Number)
	- configure code/conf/mamba_dlp.conf
	- Create a new role that has read access to all buckets. example: mamba_lambda_read_buckets
	- Create  a Lambda role that allows mamba_dlp to assume "mamba_lambda_read_buckets"
	- Create lambda_code.zip:
		```sh
		$cd code
		$chmod +rw *
		$zip -r lambda_code.zip *
		```
	- Create lambda "mamba_dlp()" in AWS account and upload lambda_code.zip
	- configure lambda handler to point to mamba_dlp.lambda_handler
	- Configure all buckets to invoke mamba_dlp() upon creating uploading or updating a new file

