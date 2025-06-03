import logging
import boto3

class AWSManager(object):
    def __init__(self):
        try:
            self.s3 = boto3.client('s3')
            self.bucket_name = 'project-bloc2-jack-lecomte'
        except Exception as e:
            logging.error("Error logging into AWS S3 client : %s", e)


    def upload_data_to_s3(self, file_name):
        try:
            self.s3.upload_file(f"data/raw/{file_name}", self.bucket_name, f"raw_{file_name}")
            print(f"{file_name} uploaded to s3")
        except Exception as e:
            logging.error("Error uploading data to S3 : %s", e)