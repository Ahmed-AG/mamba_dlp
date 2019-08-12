import mmap
import re
import json
import os

import state_object

class finder():
    def __init__(self, dynamo_table):
        self.data_found = {'data_found':[]}
        self.secret_regexs = {'secret_regexs':[
            {
            'data_type' : 'payment_card',
            'regex' : r'(?i)4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011\
                    |5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}\
                    |(?:2131|1800|35\d{3})\d{11}',
            'remove_char' : ['-' , ' ' , ','],
            'exceptions' : []
            },
            {
            'data_type' : 'email_address',
            'regex' : r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+',
            'remove_char' :[],
            'exceptions' : []
            }
            ]}

        self.state = state_object.sensitive_data(dynamo_table)

        return


    def scan_objects(self,data_source):

        for object in data_source.objects['objects']:
            local_object=data_source.download_key(object)
            if (os.stat(local_object).st_size != 0):
                self.scan_secrets(local_object,object,self.secret_regexs['secret_regexs'])
            else:
                print("EMPTY FILE!")
        return self.data_found

    def scan_secrets(self,local_object,object,secret_regexs):
        dynamo_response=""

        with open(local_object, 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
            for idx, line in enumerate(iter(s.readline, b"")):
                for search_regex in secret_regexs:
                    #remove certain chars
                    for remove_char in search_regex['remove_char']:
                        line=str(line).replace(remove_char,"")

                    search_result=re.findall(search_regex['regex'], str(line))

                    if len(search_result) != 0:
                        #print("SECRET DATA FOUND!!")

                        masked_data = self.mask_data(search_result , search_regex['data_type'])
                        
                        #add data to local object
                        self.data_found['data_found'].append({'object_id' : object['object_id'],
                            'object_type' : object['object_type'],
                            'data' : masked_data,
                            'data_type' : search_regex['data_type'],
                            'location' : str(idx)
                            })
                        
                        #add data to Dynamo
                        data_object = {'object_id' : object['object_id'],
                            'object_type' : object['object_type'],
                            'data' : masked_data,
                            'data_type' : search_regex['data_type'],
                            'location' : str(idx)
                            }
                        dynamo_response = self.state.save_sensitive_object(data_object)
                        
                        #Start action
                        
        return dynamo_response

    def mask_data(self , data_set , data_type):
        masked_data= []

        for data in data_set:

            if data_type == "payment_card":
                masked_data.append("************" + data[-4:])

            elif data_type == "email_address":
                masked_data.append(data[0] + "**@**" + data[len(data)-1])
        
        return masked_data


class pii_finder():
    def __init__(self):
        print("test")
        return
