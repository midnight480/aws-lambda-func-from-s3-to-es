# aws-lambda-func-from-s3-to-es
the CSV file saved in AWS S3 and create a document for each line of the CSV with the Index name specified in ElasticSearch.

## Develop Enviorment

* CentOS Linux 7
* Python 2.7.5
* pip 20.2.3 (python 2.7)
* AWS Lambda
* ElasticSearch Service 7.7.0

## pip install list

```
# cd ${WORKSPACE}
#
# pip install s3fs -t .
#
# pip install requests_aws4auth -t .
#
# pip install elasticsearch -t .
```
