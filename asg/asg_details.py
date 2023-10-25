import boto3
from utils.logger import Logger
from utils.utilities import read_tags_from_file


class ASGDetails:
    def __init__(self, region):
        self.client = boto3.client('autoscaling', region_name=region)
        self.region = region
        self.asgs = []

    def fetch_asgs_by_application_tag(self, tag_input_file):
        """Fetch ASGs based on application tags provided in the input file."""
        application_tags = read_tags_from_file(tag_input_file)
        paginator = self.client.get_paginator('describe_auto_scaling_groups')

        for page in paginator.paginate(PaginationConfig={'PageSize': 100}):
            for asg in page['AutoScalingGroups']:
                for tag in asg['Tags']:
                    if tag['Key'] == 'application' and tag['Value'] in application_tags:
                        self.asgs.append(asg)
        return self.asgs

    def identify_az_type(self, asg):
        """Identify if the ASG is multi-AZ or single-AZ."""
        if len(asg['AvailabilityZones']) > 1:
            return "multi-az"
        return "single-az"

    def filter_asgs_by_az(self, az):
        """Filter the ASGs by a particular Availability Zone."""
        filtered_asgs = [asg for asg in self.asgs if az in asg['AvailabilityZones']]
        return filtered_asgs

    # Additional methods as per your requirements can be added here.

# Usage example:
# asg_detail_obj = ASGDetails('us-west-2')
# asgs = asg_detail_obj.fetch_asgs_by_application_tag('tag_input.txt')
# for asg in asgs:
#     print(asg_detail_obj.identify_az_type(asg))
