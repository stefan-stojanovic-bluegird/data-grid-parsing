import boto3
import logging

def add_to_s3(filename,object_name):
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename="log.log")

    logging.log("Adding {}".format(object_name))
    s3_client = boto3.client("s3")
    s3_bucket = "data-grid"

    try:
        reponse = s3_client.upload_file(filename,s3_bucket,object_name)
    except ClientError as e:
        logging.log("Retrying for {}".format(object_name))
        return add_to_s3(filename,object_name)

    logging.log("Success")

