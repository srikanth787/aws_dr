import boto3

class CredentialsHandler:
    def __init__(self, profile_name=None, region_name='us-west-2', logger=None, role_arn=None, role_session_name='my_session'):
        self.logger = logger
        self.session = self.create_session(profile_name, region_name)
        if role_arn:
            self.assume_role(role_arn, role_session_name)

    def create_session(self, profile_name, region_name):
        """
        Create a boto3 session.

        :param profile_name: AWS CLI profile name.
        :param region_name: AWS region.
        :return: boto3 Session.
        """
        try:
            if profile_name:
                session = boto3.Session(profile_name=profile_name, region_name=region_name)
            else:
                session = boto3.Session(region_name=region_name)
            return session
        except Exception as e:
            self.logger.error(f"Error creating boto3 session: {e}")
            raise e

    def assume_role(self, role_arn, role_session_name):
        """
        Assume an AWS role using STS.

        :param role_arn: ARN of the role to assume.
        :param role_session_name: Session name.
        """
        try:
            sts_client = self.session.client('sts')
            assumed_role = sts_client.assume_role(
                RoleArn=role_arn,
                RoleSessionName=role_session_name
            )
            self.session = boto3.Session(
                aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
                aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
                aws_session_token=assumed_role['Credentials']['SessionToken']
            )
        except Exception as e:
            self.logger.error(f"Error assuming role {role_arn}: {e}")
            raise e

    def client(self, service_name, max_attempts=5, mode='standard'):
        """
        Create a boto3 client for the specified service.

        :param service_name: AWS service name, e.g., 'ec2', 'autoscaling'.
        :param max_attempts: Maximum number of retry attempts.
        :param mode: Retry mode. Valid values are 'legacy' or 'standard'. Default is 'standard'.
        :return: boto3 client.
        """
        try:
            retry_config = Config(
                retries={
                    'max_attempts': max_attempts,
                    'mode': mode
                }
            )
            return self.session.client(service_name, config=retry_config)
        except Exception as e:
            self.logger.error(f"Error creating boto3 client for {service_name}: {e}")
            raise e

    def resource(self, service_name):
        """
        Create a boto3 resource client for the specified service.

        :param service_name: AWS service name, e.g., 'ec2'.
        :return: boto3 resource.
        """
        try:
            return self.session.resource(service_name)
        except Exception as e:
            self.logger.error(f"Error creating boto3 resource for {service_name}: {e}")
            raise e
