# ec2/ec2_details.py

import boto3
import csv
from utils.logger import CustomLogger
from datetime import datetime
import os

logger = CustomLogger(__name__).get_logger()


class EC2Details:
    def __init__(self, session):
        self.session = session
        self.ec2 = self.session.resource('ec2')
        self.client = self.session.client('autoscaling')

    def _get_asg_instance_ids(self):
        """Retrieve all instance IDs that are part of any ASG."""
        instance_ids = []
        paginator = self.client.get_paginator('describe_auto_scaling_instances')
        for page in paginator.paginate():
            for instance in page['AutoScalingInstances']:
                instance_ids.append(instance['InstanceId'])
        return instance_ids

    def _get_tags_from_file(self, tag_file_path):
        """Parse the tag file and return a list of tag filters."""
        tag_filters = []
        try:
            with open(tag_file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    key, value = line.strip().split('=')
                    tag_filters.append({'Name': f'tag:{key}', 'Values': [value]})
            return tag_filters
        except Exception as e:
            logger.error(f"Error reading tag file: {e}")
            return []

    def get_instances_not_in_asg_with_tags(self, availability_zone, tag_file_path):
        asg_instance_ids = set(self._get_asg_instance_ids())
        tag_filters = self._get_tags_from_file(tag_file_path)

        filters = [
            {
                'Name': 'availability-zone',
                'Values': [availability_zone]
            }
        ]
        filters.extend(tag_filters)  # Add tag filters

        try:
            all_instances = list(self.ec2.instances.filter(Filters=filters))
            # Now, filter out instances that are in ASGs
            non_asg_instances = [instance for instance in all_instances if instance.id not in asg_instance_ids]
            return non_asg_instances
        except Exception as e:
            logger.error(f"Error fetching instances: {e}")
            return []

    def _generate_file_path(self, az, account, region, filename_prefix):
        current_date = datetime.now().strftime('%Y-%m-%d')
        directory_path = f"output/{account}/{region}/{az}/{current_date}/"

        # Ensure the directory exists
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        return os.path.join(directory_path, f"{filename_prefix}.csv")

    def display_instances(self, availability_zone, account, region, tag_file_path):
        instances = self.get_instances_not_in_asg_with_tags(availability_zone, tag_file_path)
        file_path = self._generate_file_path(availability_zone, account, region, "ec2_instances_not_in_asg")
        self._write_to_csv(instances, file_path)

    def _write_to_csv(self, instances, file_path):
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['instance_id', 'private_ip', 'instance_type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # write the header
            for instance in instances:
                writer.writerow({
                    'instance_id': instance.id,
                    'private_ip': instance.private_ip_address,
                    'instance_type': instance.instance_type
                })
            logger.info(f"Data written to {file_path}")
