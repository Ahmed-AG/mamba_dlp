import boto3
from boto3.dynamodb.conditions import Key, Attr
import decimal
import json
import botocore


dynamodb = boto3.resource('dynamodb')

class sensitive_data():
    def __init__(self , dynamo_table):
        self.dynamo_table = dynamo_table
        return

    def load_sensitive_objects(self):
        print(response)
        return self.sensitive_data

    def save_sensitive_data(self, data_object):
        return response

    def load_sensitive_object(self,object_id):

        table = dynamodb.Table(self.dynamo_table)
        response = table.query(
            KeyConditionExpression=Key('object_id').eq(object_id)
        )

        return response['Items']

    def save_sensitive_object(self,data_object):
        response={}
        try:
            table = dynamodb.Table(self.dynamo_table)
            response = table.put_item(
            Item={
                'object_type': data_object['object_type'],
                'object_id': data_object['object_id'], 
                'location': decimal.Decimal(data_object['location']), 
                'data': data_object['data'], 
                'data_type': data_object['data_type']
                }
            )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "AccessDeniedException":
                print("WARNING: " + e.response['Error']['Message'])
            else:
                print(json.dumps(e.response, sort_keys=True , indent=2))
                raise
        return response