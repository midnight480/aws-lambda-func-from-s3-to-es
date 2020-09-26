# coding: utf-8

def lambda_handler(event, context):
    import os
    import boto3
    import csv
    import s3fs
    from requests_aws4auth import AWS4Auth
    from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
    from botocore.exceptions import ClientError

    # get credential
    region = '' # e.g. us-west-1
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    # s3 bucket info
    s3 = s3fs.S3FileSystem(anon=False)
    #bucket = record['s3']['bucket']['name']
    #key = record['s3']['object']['key']
    # Test Bucket 
    #bucket = '' # e.g. from-s3-to-es-sample
    #key = '' # e.g. data.csv
    # input file 
    input_file = os.path.join(bucket, key)
    target_file = s3.open(input_file, 'r')

    # prepare for elasticsearch
    reader_obj = csv.DictReader(target_file)
    index_name = "" # e.g. index-csv-s3
    host = 'XXXXXXXXXXXXXXX.${Region}.es.amazonaws.com' # NOTE! not include https://

    # connect to elasticsearch
    es = Elasticsearch(
        hosts=[{'host': host , 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    # debug for CloudWatch Logs 
    print('--------1. Lambda Connect to ElasticSearch Service-----------')
    print(es.info())
    print('--------2. Check Reading Obejcts-----------')
    print(reader_obj) # e.g <csv.DictReader instance at 0x999999999>
    print('--------3. Transfer to ElasticSearch-----------')
    for row in reader_obj:
        # Prepare for id
        doc = row
        # Set id of Documents
        date = doc['date']
        # Transfer CSV Data of S3 to ElasticSearch      
        es.index( index = index_name, id = date, body = doc)
