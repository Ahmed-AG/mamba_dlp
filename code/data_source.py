
import boto3
import aws
import json
import botocore

class s3():
    def __init__(self,aws_accounts,aws_role):

        self.aws_accounts=aws_accounts
        self.files = ""
        self.data_discovered=""
        self.aws_role=aws_role
#        self.objects=self.find_objects()


    def find_objects(self):

        objects={'objects':[]}

        for aws_account in self.aws_accounts:
    
            #assumedRoleObject=aws.assume_role(aws_account,self.aws_role)         
            
            #client = boto3.client('s3',
            #    aws_access_key_id = assumedRoleObject['Credentials']['AccessKeyId'],
            #    aws_secret_access_key = assumedRoleObject['Credentials']['SecretAccessKey'],
            #    aws_session_token = assumedRoleObject['Credentials']['SessionToken']
            #)
            client = boto3.client('s3')
            try:
                buckets=client.list_buckets()

                for bucket in buckets['Buckets']:
                    keys = self.list_keys(aws_account,bucket['Name'])
                    for key in keys:
                        object_id = aws_account + ":" + bucket['Name'] + ":" + key['Key']
                        
                        objects['objects'].append({'object_id' : object_id,
                             'object_type' : 's3',
                             'aws_account': aws_account,
                             'bucket': bucket['Name'], 
                             'key': key['Key']
                            }
                            )
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "AccessDenied":
                    print(json.dumps(e.response, sort_keys=True , indent=2))
                else:
                    print(e.response)
                    raise

                    #print(json.dumps(objects))
                    #break

                #print(json.dumps(objects))
                #break
                
        return objects

    def list_keys(self,aws_account,bucket):

        #assumedRoleObject = aws.assume_role(aws_account,self.aws_role)
        #client = boto3.client('s3',
        #    aws_access_key_id = assumedRoleObject['Credentials']['AccessKeyId'],
        #    aws_secret_access_key = assumedRoleObject['Credentials']['SecretAccessKey'],
        #    aws_session_token = assumedRoleObject['Credentials']['SessionToken']
        #)
        client = boto3.client('s3')
        objects = client.list_objects(
            Bucket = bucket
        )

        if ('Contents' in objects):
            return objects['Contents']
        else:
            return []


    def download_key(self,object):
        #assumedRoleObject=aws.assume_role(object['aws_account'],self.aws_role) 

        #s3 = boto3.resource('s3',
        #    aws_access_key_id = assumedRoleObject['Credentials']['AccessKeyId'],
        #    aws_secret_access_key = assumedRoleObject['Credentials']['SecretAccessKey'],
        #    aws_session_token = assumedRoleObject['Credentials']['SessionToken']
        #    )
        s3 = boto3.resource('s3')
        
        bucket = object['bucket']
        key = object['key']
        download_file = "/tmp/target_object"

        
        try:
            print("Scanning: " + object['bucket']  + ":" + object['key'])
            response = s3.Bucket(bucket).download_file(key, download_file)

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return "Object: " + key + " in " + bucket + "does not exist."
            elif e.response['Error']['Code'] == "403":
                print(e.response['Error']['Code'] + ":" + e.response['Error']['Message'])
            else:
                raise

        return download_file
    def cleaup_object(self,file):

        #delete file

        return

    def scan_file(self,file):

        for finder in self.data_finders:
            scan_results=finder.scan(file)
            if scan_result!= -1:
                self.data_discovered=self.data_discovered + "file information + data discovered + line discovered"

        #scans the file using the object self.data_finders
        #attach scan results to the self.files_list
