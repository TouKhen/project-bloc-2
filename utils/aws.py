import logging
import boto3
import pymysql
import sys
import os

class AWSManager(object):
    def __init__(self, type='s3'):
        if type == 's3':
            try:
                self.s3 = boto3.client('s3')
                self.bucket_name = 'project-bloc2-jack-lecomte'
            except Exception as e:
                logging.error("Error logging into AWS S3 client : %s", e)
        elif type == 'rds':
            self.ENDPOINT = "database-1.cfk6esosclq7.eu-north-1.rds.amazonaws.com"
            self.PORT = "3306"
            self.USER = "admin"
            self.REGION = "eu-north-1b"
            self.DBNAME = "database-1"
            os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

            # gets the credentials from .aws/credentials
            session = boto3.Session(profile_name='default')
            client = session.client('rds', region_name=self.REGION)

            token = client.generate_db_auth_token(DBHostname=self.ENDPOINT,
                                                  Port=self.PORT, DBUsername=self.USER,
                                                  Region=self.REGION)

            try:
                self.conn = pymysql.connect(
                    auth_plugin_map={'mysql_clear_password': None},
                    host=self.ENDPOINT, user=self.USER, port=self.PORT,
                    database=self.DBNAME, ssl_ca='SSLCERTIFICATE',
                    ssl_verify_identity=True)
                self.cur = self.conn.cursor()
            except Exception as e:
                print("Database connection failed due to {}".format(e))


    def create_table_rds(self, file_name='data'):
        conn = pymysql.connect(
            auth_plugin_map={'mysql_clear_password': None},
            host=self.ENDPOINT, user=self.USER, port=self.PORT,
            database=self.DBNAME, ssl_ca='SSLCERTIFICATE',
            ssl_verify_identity=True)
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NULL,
            link TEXT NULL,
            company VARCHAR(255) NULL,
            location VARCHAR(255) NULL,
            hours INT NULL,
            level VARCHAR(255) NULL,
            salary_text VARCHAR(255) NULL,
            salary FLOAT NULL,
        )
        """)
        cur.commit()


    def upload_data_to_s3(self, file_name):
        try:
            self.s3.upload_file(f"data/raw/{file_name}", self.bucket_name, f"raw_{file_name}")
            print(f"{file_name} uploaded to s3")
        except Exception as e:
            logging.error("Error uploading data to S3 : %s", e)