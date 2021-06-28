# TA-dynamodb-get Description

*** NOTE *** 
This TA is NOT production ready.

This TA allows you to ingest DynamoDB data via the dynamodb_get input type and it also supplies a custom streaming command (dynamoget) that will allow a user to query DynamoDB via a Splunk search to enrich (lookup) events.

## dynamodb_get Input Configuration

Configuration of the dynamodb_get input type includes the following attributes:

- Name - Name of the input
- Interval - How often to collect DynamoDB data
- Index - target index for ingestion
- AWS Region - The region that your DynamoDB table is hosted in (us-east-1 for example)\
- AWS Key ID - The AWS Key to use for access to the DynamoDB table
- AWS Secret - The AWS secret to use with the AWS Key ID
- DynamoDB Table Name - The name of the DynamoDB table you wish to query
- Table Query String - The full string to use to query the table - for further details see the "Querying" section below

### Querying

At time of writing, the input only supports basic scan and query strings. For more details and some examples [see - AWS Developer Guide]( https://docs.amazonaws.cn/en_us/amazondynamodb/latest/developerguide/GettingStarted.PHP.04.html)

#### Query Example

You can only use simple Key queries to search for data currently.

Example:
> table.query(IndexName = <INDEX_NAME>,KeyConditionExpression = Key(<KEY_NAME>).eq(<QUERY_STRING>))

#### Scan Example

You can only use simple scan strins with a filter expression currently.

Example:
> table.scan(FilterExpression=Attr(<ATTR_NAME>).eq(<QUERY_STRING>))

## dynamoget Streaming Command Usage

The dynamoget command supports the following command options:

- Input - The name of the input to use to gather the needed credentials to access the DynamoDB table. 
- Table - The table name you wish to query
- Query - The query string you wish to use to gather data
- Source field - The field to use in your search to match against a field in DynamoDB
- Dynamo Match Field - The field in DynamoDB to match against the Source Field

Example:

> index=dynamo email_address=* | dynamoget region="us-east-1" input="us_east_1_health_id" table="health_id" query="table.query(IndexName = \"email-index\",KeyConditionExpression = Key(\"email\").eq(\"adalton@test.com\"))" source_field="email_address" dynamo_match_field="email" | table email_address, DYNAMO*

We are searching for events containing an email_address field in the dynamo index. We then pipe that output to the dynamoget command. The dynamoget command will run the query specified in the "query" field and attempt to match the contents from the "source" field with the "dynamo_match_field" contents. If there is a match the dynamo fields for the match will be added to the original event with the prefix DYNAMO_ . In addition the DYNAMO_MATCH field will be set to "true". If no match is found, the DYNAMO_MATCH field will be set to "false" and no further fields will be added>

Example output can be seen below:

![alt text](https://github.com/bantex01/TA-dynamodb-get/blob/main/README/dynamoget_output.png?raw=true)

### Accessing the DynamoDB table from the dynamoget command

In order to query DynamoDB the dynamoget command requires AWS credentials. The "input" field tells the command what configured input to use to gather the credentials required.

If you do not wish to use the dynamodb_get input to periodically collect and ingest DynamoDB data you will still need to configure an input in order to use the dynamoget custom command. In this scenario, configure the input for this purpose but leave it disabled.
