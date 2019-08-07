<BETA>
mamba_dlp
=========

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

Getting Started 
----------------

- **Scan all files in all buckets:**
	```sh
	$python3 code/mamba_dlp.py --run full_scan
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

- **Scan a single file:**

	```sh
	python3 code/mamba_dlp.py --run scan_object --object \
		"{\"objects\" : [{\"object_id\" : \"<AWS_ACCOUNT>:<BUCKET:KEY\",\
		 \"object_type\" : \"s3\",\
		 \"aws_account\": \"<AWS_ACCOUNT>\",\
		 \"bucket\": \"<BUCKET>\", \"key\": \"<KEY>\" }]}"
	```



