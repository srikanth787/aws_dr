import boto3
import json
from utils.logger import logger
from utils.utilities import read_tags_from_file


class ASGProcessManager:
    def __init__(self, region):
        self.client = boto3.client('autoscaling', region_name=region)
        self.asgs = []
        self.region = region

    def fetch_asgs_by_application_tag(self, tag_input_file):
        application_tags = read_tags_from_file(tag_input_file)
        paginator = self.client.get_paginator('describe_auto_scaling_groups')

        for page in paginator.paginate(PaginationConfig={'PageSize': 100}):
            for asg in page['AutoScalingGroups']:
                for tag in asg['Tags']:
                    if tag['Key'] == 'application' and tag['Value'] in application_tags:
                        self.asgs.append(asg)
        return self.asgs

    def identify_az_type(self, asg):
        if len(asg['AvailabilityZones']) > 1:
            return "multi-az"
        return "single-az"

    def store_asg_states(self, asg_name):
        response = self.client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name],
            MaxRecords=1
        )
        asg = response['AutoScalingGroups'][0]
        with open("outputs/original_asg_states.json", "a") as file:
            file.write(json.dumps({asg_name: asg['Status']}))

    def suspend_asg_processes(self, asg_name):
        self.store_asg_states(asg_name)
        self.client.suspend_processes(AutoScalingGroupName=asg_name)
        logger.info(f"Suspended processes for ASG: {asg_name}")

    def resume_asg_processes(self, asg_name):
        self.client.resume_processes(AutoScalingGroupName=asg_name)
        logger.info(f"Resumed processes for ASG: {asg_name}")

    def retrieve_original_state_and_resume(self, asg_name):
        with open("outputs/original_asg_states.json", "r") as file:
            states = json.load(file)
            original_state = states.get(asg_name, {})

        # Here, you can check the original state and decide what to do
        # For simplicity, we'll just resume the processes.
        self.resume_asg_processes(asg_name)
