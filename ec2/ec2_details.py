import boto3
import csv
import os
from datetime import datetime


class EC2Details:

    def __init__(self, session, tags=None, availability_zone=None):
        """
        Initialize the EC2Details class.

        Parameters:
        - session: boto3 Session.
        - tags: Dictionary of tag keys and values for filtering EC2 instances.
        - availability_zone: The availability zone to filter the EC2 instances.
        """
        self.session = session
        self.ec2_client = session.client('ec2')
        self.tags = tags or {}
        self.availability_zone = availability_zone

    def _get_instances(self):
        """
        Get EC2 instances based on tags and availability zone.
        """
        filters = [
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]

        if self.availability_zone:
            filters.append({'Name': 'availability-zone', 'Values': [self.availability_zone]})

        if self.tags:
            for key, value in self.tags.items():
                filters.append({'Name': f'tag:{key}', 'Values': [value]})

        paginator = self.ec2_client.get_paginator('describe_instances')
        response_iterator = paginator.paginate(Filters=filters, PaginationConfig={'PageSize': 100})

        for page in response_iterator:
            for reservation in page['Reservations']:
                for instance in reservation['Instances']:
                    yield instance

    def write_to_csv(self, account, region, az):
        """
        Write EC2 details to a CSV file.
        """
        current_date = datetime.now().strftime('%Y-%m-%d')
        base_path = f"outputs/{account}/{region}/{az}/{current_date}"
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        csv_file = os.path.join(base_path, "ec2_details.csv")

        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Instance ID", "Private IP Address", "Instance Type"])

            for instance in self._get_instances():
                writer.writerow(
                    [instance["InstanceId"], instance.get("PrivateIpAddress", ""), instance["InstanceType"]])

# Example usage:
# session = boto3.Session(region_name="us-west-2")
# ec2_details = EC2Details(session, tags={"Name": "my-instance"}, availability_zone="us-west-2a")
# ec2_details.write_to_csv("123456789012", "us-west-2", "us-west-2a")
