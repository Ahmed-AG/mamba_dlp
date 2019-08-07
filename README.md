#mamba_dlp


mamba_dlp
=========

Mamba_dlp is a tool for searching for sensitive data in cloud infrastructures.

The key features of Mamba_dlp:

- **Search for sensitive data**: using customizable regex, mamba_dlp scans through data sources and reports any sensitive data

Getting Started 
----------------

- **Scan all files in all buckets:**
	python3 code/mamba_dlp.py --run full_scan

- **Scan in realtime:**

1 - Create lambda: mamba_dlp()
2 - Configure all buckets to invoke mamba_dlp() upon creating uploading or updating a new file
3 - Create a new role that has read access to all buckets. example: mamba_lambda_read_buckets
4 - Create  a Lambda role that allows mamba_dlp to assume "mamba_lambda_read_buckets"

- **Scan a single file:**

	python3 code/mamba_dlp.py --run scan_object --object \
		"{\"objects\" : [{\"object_id\" : \"<AWS_ACCOUNT>:<BUCKET:KEY\",\
		 \"object_type\" : \"s3\",\
		 \"aws_account\": \"<AWS_ACCOUNT>\",\
		 \"bucket\": \"<BUCKET>\", \"key\": \"<KEY>\" }]}"



