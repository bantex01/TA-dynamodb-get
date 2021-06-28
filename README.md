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

![alt text](https://github.com/bante01/TA-dynamodb-get/README/blob/main/dynamoget_output.png?raw=true)

