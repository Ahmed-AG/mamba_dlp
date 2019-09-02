
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

```sh
$python3 code/mamba_dlp.py --run scan_object --bucket bucket --key cards_and_email.txt --aws_account ************
                           _                _ _       
                          | |              | | |      
 _ __ ___   __ _ _ __ ___ | |__   __ _   __| | |_ __  
| '_ ` _ \ / _` | '_ ` _ \| '_ \ / _` | / _` | | '_ \ 
| | | | | | (_| | | | | | | |_) | (_| || (_| | | |_) |
|_| |_| |_|\__,_|_| |_| |_|_.__/ \__,_| \__,_|_| .__/ 
                                    ______     | |    
                                   |______|    |_|    
Scanning: bucket:cards_and_email.txt
Action: bucket Tagged: 
{
 "TagSet": [
  {
   "Key": "pci_sensitive_data",
   "Value": "true"
  }
 ]
}
Action: bucket Tagged: 
{
 "TagSet": [
  {
   "Key": "pci_sensitive_data",
   "Value": "true"
  },
  {
   "Key": "email_address",
   "Value": "true"
  }
 ]
}
Sensitive Data Found:
{
  "data_found": [
    {
      "data": [
        "************9534"
      ],
      "data_type": "payment_card",
      "location": "1",
      "object_id": "***********:bucket:cards_and_email.txt",
      "object_type": "s3"
    },
    {
      "data": [
        "a**@**m"
      ],
      "data_type": "email_address",
      "location": "2",
      "object_id": "***********:bucket:cards_and_email.txt",
      "object_type": "s3"
    }
  ]
}
$
```

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




- **Realtime Deployment:**
	--run deploy_realtime option will do three things:
		1) Deploy mamba_dlp as a lambda function
		2) Configure all buckets to call mamba_dlp upon file uploads to scan that file
		3) Build Dynamo table
	
	To configure this option run the following:

	```sh
	$python3 code/mamba_dlp.py --run deploy_realtime
		                           _                _ _       
		                          | |              | | |      
		 _ __ ___   __ _ _ __ ___ | |__   __ _   __| | |_ __  
		| '_ ` _ \ / _` | '_ ` _ \| '_ \ / _` | / _` | | '_ \ 
		| | | | | | (_| | | | | | | |_) | (_| || (_| | | |_) |
		|_| |_| |_|\__,_|_| |_| |_|_.__/ \__,_| \__,_|_| .__/ 
		                                    ______     | |    
		                                   |______|    |_|     
	Enter bucket name to be used for Cloudformation template: bucket9999
	*** Running deployment script: deploy/deploy_realtime.sh
	  adding: actions.py (deflated 70%)
	  adding: aws.py (deflated 38%)
	  adding: conf/ (stored 0%)
	  adding: conf/mamba_dlp.conf (deflated 65%)
	  adding: conf/mamba_dlp_policy.yaml.sample (deflated 61%)
	  adding: conf/mamba_dlp_policy.yaml (deflated 61%)
	  adding: conf/mamba_dlp.conf.samle (deflated 67%)
	  adding: data_finder.py (deflated 70%)
	  adding: data_source.py (deflated 75%)
	  adding: mamba_dlp.py (deflated 71%)
	  adding: state_object.py (deflated 65%)
	upload: ./lambda_code.zip to s3://bucket9999/lambda_code.zip     
	Waiting for changeset to be created..
	Waiting for stack create/update to complete
	Successfully created/updated stack - mamba-realtime-stack
	*** Configuring: arn:aws:s3:::bucket8888
	lambda_permission added!
	bucket_notification added!
	*** Configuring: arn:aws:s3:::bucket9999
	lambda_permission added!
	bucket_notification added!
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

