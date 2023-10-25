import boto3
import csv
import os
from utils.credentials_handler import AWSHandler
from utils.utilities import Utilities
from utils.logger import Logger


class EC2Details:

    def __init__(self, account, region, az):
        self.account = account
        self.region = region
        self.az = az
        self.session = AWSHandler().create_session(account, region)
        self.ec2_client = self.session.client('ec2')
        self.logger = Logger(account, region, az).get_logger()
        self.utilities = Utilities(account, region, az)

    def filter_instances(self, tags):
        """
        Filter EC2 instances based on tags, availability zone, and if they're running.
        """
        tag_filters = [{'Name': f'tag:{key}', 'Values': [value]} for key, value in tags.items()]
        az_filter = {'Name': 'availability-zone', 'Values': [self.az]}
        running_filter = {'Name': 'instance-state-name', 'Values': ['running']}

        try:
            response = self.ec2_client.describe_instances(Filters=[*tag_filters, az_filter, running_filter])
            return [instance for reservation in response['Reservations'] for instance in reservation['Instances']]
        except Exception as e:
            self.logger.error(f"Error fetching EC2 instances: {str(e)}")
            return []

    def write_to_csv(self, instances):
        """
        Write EC2 instance details to a CSV file.
        """
        file_path = self.utilities.get_output_path('ec2_details.csv')

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Instance ID', 'Private IP Address', 'Instance Type'])

            for instance in instances:
                writer.writerow(
                    [instance['InstanceId'], instance.get('PrivateIpAddress', 'N/A'), instance['InstanceType']])

        self.logger.info(f"EC2 details written to: {file_path}")

    def fetch_and_store(self, tag_file):
        """
        Fetch EC2 instances and write them to a CSV file.
        """
        tags = self.utilities.read_tags_from_file(tag_file)
        instances = self.filter_instances(tags)
        if instances:
            self.write_to_csv(instances)
        else:
            self.logger.info("No matching EC2 instances found.")

