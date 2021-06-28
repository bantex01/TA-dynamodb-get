
# encoding = utf-8

import os
import sys
import time
import datetime

import re
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''

def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # aws_region = definition.parameters.get('aws_region', None)
    # aws_key_id = definition.parameters.get('aws_key_id', None)
    # aws_secret = definition.parameters.get('aws_secret', None)
    # dynamodb_table_name = definition.parameters.get('dynamodb_table_name', None)
    # table_query_string = definition.parameters.get('table_query_string', None)
    pass

def collect_events(helper, ew):
    
    sourcetype = helper.get_sourcetype()
    helper.log_critical("source type is "+str(sourcetype))
    index = helper.get_output_index()
    helper.log_critical("index is "+str(index))
    
    date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    
    opt_aws_region = helper.get_arg('aws_region')
    opt_aws_key_id = helper.get_arg('aws_key_id')
    opt_aws_secret = helper.get_arg('aws_secret')
    opt_dynamodb_table_name = helper.get_arg('dynamodb_table_name')
    opt_table_query = helper.get_arg('table_query_string')

    # Let's set up the env variables needed
    
    os.environ["AWS_DEFAULT_REGION"] = opt_aws_region
    os.environ["AWS_ACCESS_KEY_ID"] = opt_aws_key_id
    os.environ["AWS_SECRET_ACCESS_KEY"] = opt_aws_secret
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(opt_dynamodb_table_name)
    
    helper.log_critical("query string is "+str(opt_table_query))
    response = eval(opt_table_query)

    helper.log_critical("LOGGER: return is "+str(response))
    
    for record in response['Items']:
        event_string = ""
        record=str(record)
        event_array = record.split(",")
        for event_field in event_array:
            a = re.search('.+?\'(.+?)\':.+?\'(.+?)\'',event_field)
            event_string = event_string + " " + a.group(1) + "=" + a.group(2)
    
        event = helper.new_event(event_string, time=date, host="dynamo", index=index, source="custom_dyn", sourcetype=sourcetype, done=True, unbroken=True)
        ew.write_event(event)
    
    
    """Implement your data collection logic here

    # The following examples get the arguments of this input.
    # Note, for single instance mod input, args will be returned as a dict.
    # For multi instance mod input, args will be returned as a single value.
    opt_aws_region = helper.get_arg('aws_region')
    opt_aws_key_id = helper.get_arg('aws_key_id')
    opt_aws_secret = helper.get_arg('aws_secret')
    opt_dynamodb_table_name = helper.get_arg('dynamodb_table_name')
    opt_table_query_string = helper.get_arg('table_query_string')
    # In single instance mode, to get arguments of a particular input, use
    opt_aws_region = helper.get_arg('aws_region', stanza_name)
    opt_aws_key_id = helper.get_arg('aws_key_id', stanza_name)
    opt_aws_secret = helper.get_arg('aws_secret', stanza_name)
    opt_dynamodb_table_name = helper.get_arg('dynamodb_table_name', stanza_name)
    opt_table_query_string = helper.get_arg('table_query_string', stanza_name)

    # get input type
    helper.get_input_type()

    # The following examples get input stanzas.
    # get all detailed input stanzas
    helper.get_input_stanza()
    # get specific input stanza with stanza name
    helper.get_input_stanza(stanza_name)
    # get all stanza names
    helper.get_input_stanza_names()

    # The following examples get options from setup page configuration.
    # get the loglevel from the setup page
    loglevel = helper.get_log_level()
    # get proxy setting configuration
    proxy_settings = helper.get_proxy()
    # get account credentials as dictionary
    account = helper.get_user_credential_by_username("username")
    account = helper.get_user_credential_by_id("account id")
    # get global variable configuration
    global_userdefined_global_var = helper.get_global_setting("userdefined_global_var")

    # The following examples show usage of logging related helper functions.
    # write to the log for this modular input using configured global log level or INFO as default
    helper.log("log message")
    # write to the log using specified log level
    helper.log_debug("log message")
    helper.log_info("log message")
    helper.log_warning("log message")
    helper.log_error("log message")
    helper.log_critical("log message")
    # set the log level for this modular input
    # (log_level can be "debug", "info", "warning", "error" or "critical", case insensitive)
    helper.set_log_level(log_level)

    # The following examples send rest requests to some endpoint.
    response = helper.send_http_request(url, method, parameters=None, payload=None,
                                        headers=None, cookies=None, verify=True, cert=None,
                                        timeout=None, use_proxy=True)
    # get the response headers
    r_headers = response.headers
    # get the response body as text
    r_text = response.text
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = response.json()
    # get response cookies
    r_cookies = response.cookies
    # get redirect history
    historical_responses = response.history
    # get response status code
    r_status = response.status_code
    # check the response status, if the status is not sucessful, raise requests.HTTPError
    response.raise_for_status()

    # The following examples show usage of check pointing related helper functions.
    # save checkpoint
    helper.save_check_point(key, state)
    # delete checkpoint
    helper.delete_check_point(key)
    # get checkpoint
    state = helper.get_check_point(key)

    # To create a splunk event
    helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
    """

    '''
    # The following example writes a random number as an event. (Multi Instance Mode)
    # Use this code template by default.
    import random
    data = str(random.randint(0,100))
    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=data)
    ew.write_event(event)
    '''

    '''
    # The following example writes a random number as an event for each input config. (Single Instance Mode)
    # For advanced users, if you want to create single instance mod input, please use this code template.
    # Also, you need to uncomment use_single_instance_mode() above.
    import random
    input_type = helper.get_input_type()
    for stanza_name in helper.get_input_stanza_names():
        data = str(random.randint(0,100))
        event = helper.new_event(source=input_type, index=helper.get_output_index(stanza_name), sourcetype=helper.get_sourcetype(stanza_name), data=data)
        ew.write_event(event)
    '''
