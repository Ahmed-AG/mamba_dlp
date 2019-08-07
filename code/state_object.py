import boto3
from boto3.dynamodb.conditions import Key, Attr
import decimal


dynamodb = boto3.resource('dynamodb')

class sensitive_data():
    def __init__(self , dynamo_table):
        self.dynamo_table = dynamo_table
        return

    def load_sensitive_objects(self):

        print(response)


        #fetch data

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


        return response