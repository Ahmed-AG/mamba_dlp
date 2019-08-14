import boto3
import json
import botocore


class action():
    def __init__(self , config):
        self.config = config
        return

    def initiate(self , sensitive_data_object):
        
        for config_action in self.config['global_conf']['actions']:
            #print(json.dumps(sensitive_data_object, sort_keys=True , indent=2))
            #print(json.dumps(self.config, sort_keys=True , indent=2))
            
            tagged_resources=[]

            #loop over all objects
            for object in sensitive_data_object['data_found']:
                #loop over all actions (tags)
                for tag in config_action['tagging']:
                    if tag['enabled'] == "true":
                        if object['data_type'] == tag['data_type']:
                            resource_arn = self.obtain_resource_name(object)
                            resource_data_type = resource_arn + ":" + tag['data_type']
                            if not resource_data_type in tagged_resources:
                                tagging_response = self.tag_resource(resource_arn , tag['tag_set'])
                                if (tagging_response == True):
                                    tagged_resources.append(resource_arn + ":" + tag['data_type'])
                #loop over SNS notification
                #loopover initiate Lambda
            #print(tagged_resources)

        return

    def obtain_resource_name(self , object):

        #S3 objects:
        object_id = str(object['object_id'])
        #aws_account = object_id[0 , ]
        first_d = int(object_id.find(':')) + 1
        temp_str = object_id[first_d:-1] 
        second_d = int(temp_str.find(':')) 
        resource_name = temp_str[0:second_d]

        return resource_name

    def tag_resource(self , resource_arn , action_tag_set , ):
        tag_set = {}
        try:
            s3 = boto3.resource('s3')
            bucket_tagging = s3.BucketTagging(resource_arn)
        
            tag_set = bucket_tagging.tag_set
        
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "NoSuchTagSet":
                tag_set = []
            elif e.response['Error']['Code'] == "AccessDenied":
                print("Action: Tag "+ resource_arn + ": " + e.response['Error']['Message'])
                print(e.response)
                return False
            else:
                raise
        try:
            tag_set.append(action_tag_set)
            new_tag_set = {'TagSet':tag_set}
            response = bucket_tagging.put(Tagging=new_tag_set)
            print("Action: "+ resource_arn + " Tagged: " + str(new_tag_set))

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Message'] == "Cannot provide multiple Tags with the same key":
                print("Action: "+ resource_arn + " Already Tagged")
            else:
                raise

        return True
