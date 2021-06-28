#!/usr/bin/env python

import sys
import os
import re
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from splunklib.searchcommands import \
    dispatch, StreamingCommand, Configuration, Option, validators

from splunk.clilib import cli_common as cli
from splunklib.searchcommands.validators import Code


@Configuration()
class GetDynamo(StreamingCommand):

    region = Option()
    input = Option()
    table = Option()
    query = Option()
    source_field = Option()
    dynamo_match_field = Option()

    """ %(synopsis)

    ##Syntax

    %(syntax)

    ##Description

    %(description)

    """
    def prepare(self):

      global REGION 
      REGION = self.region
      global INPUT
      INPUT = self.input
      global TABLE
      TABLE = self.table
      global QUERY
      QUERY = self.query
      global SOURCE_FIELD
      SOURCE_FIELD = self.source_field
      global DYNAMO_MATCH_FIELD
      DYNAMO_MATCH_FIELD = self.dynamo_match_field

      global AWS_KEY
      global AWS_SECRET
     
      cfg = cli.getConfStanza('inputs','dynamodb_get://' + INPUT)
      AWS_KEY = cfg.get('aws_key_id')
      self.logger.debug("AWS access key is "+str(AWS_KEY)) 
            
      for secret in self.service.storage_passwords.list():
        if (secret.name == "__REST_CREDENTIAL__#TA-dynamodb-get#data/inputs/dynamodb_get:" + INPUT +"``splunk_cred_sep``1:"):
          self.logger.debug("Splunk credential match found")
          keystring = re.search("\{\"aws_secret\": \"(.+?)\"\}",secret.clear_password)
          if keystring:
            AWS_SECRET = keystring.group(1)

      

    def stream(self, records):
       
       os.environ["AWS_DEFAULT_REGION"] = REGION
       self.logger.debug("Setting AWS region to "+str(REGION))
       os.environ["AWS_ACCESS_KEY_ID"] = AWS_KEY
       self.logger.debug("Using AWS Key ID "+str(AWS_KEY))
       os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET

       # Set fields expected to be returned here otherwise the write fails (which is truly odd, need to research more on this)
       field_array = ["phone", "email", "cust_id"]

       dynamodb = boto3.resource('dynamodb')
       table = dynamodb.Table(TABLE)
       self.logger.debug("DynamoDB table set to "+str(TABLE))

       for record in records:

         #field_array = ["phone", "email", "cust_id"]
         # Initialise fields
         for field in field_array:
           record["DYNAMO_" + field] = None

         DYNAMO_MATCH = 0

         # Debug logging 
         self.logger.debug("Event/Record is "+str(record))
         self.logger.debug("Source field supplied is "+str(SOURCE_FIELD))
         self.logger.debug("Source field contains "+str(record[SOURCE_FIELD]))
         self.logger.debug("Match field supplied is "+str(DYNAMO_MATCH_FIELD))
         self.logger.debug("Table query supplied is "+str(QUERY))
         
         STRIPPED_QUERY = QUERY.replace("'","")
         self.logger.debug("Stripped query is "+str(STRIPPED_QUERY))
         response = eval(STRIPPED_QUERY)

         self.logger.debug("Dynamo response is "+str(response))

         for dynamo_record in response['Items']:
           self.logger.debug("Dynamo record is "+str(dynamo_record))
           self.logger.debug("Dynamo match field contents are "+str(dynamo_record[DYNAMO_MATCH_FIELD]))

           if(record[SOURCE_FIELD] == str(dynamo_record[DYNAMO_MATCH_FIELD])):
             DYNAMO_MATCH = 1
             self.logger.debug("Source field and dynamo field match "+str(record[SOURCE_FIELD]) + ":" + str(dynamo_record[DYNAMO_MATCH_FIELD]))
             record["DYNAMO_MATCH"] = "true"

             for field in dynamo_record:
               self.logger.debug("Event field is "+str(field) + " and value is "+str(dynamo_record[field]) + " - adding dynamo field to event output")
               field_string = "DYNAMO_" + field
               record[field_string] = dynamo_record[field]

             break

           else:
             self.logger.debug("Source field and dynamo field do not match "+str(record[SOURCE_FIELD]) + ":" + str(dynamo_record[DYNAMO_MATCH_FIELD]))

         if(DYNAMO_MATCH != 1):
           record["DYNAMO_MATCH"] = "false"

         yield record

dispatch(GetDynamo, sys.argv, sys.stdin, sys.stdout, __name__)

