import boto3
from botocore.exceptions import NoCredentialsError


class CredentialsHandler:

    def __init__(self, profile_name=None, role_arn=None):
        """
        Initialize the CredentialsHandler with an optional profile name and/or role ARN.

        Args:
        - profile_name (str): Name of the AWS profile to use. Defaults to None.
        - role_arn (str): ARN of the role to assume. Defaults to None.
        """
        self.session = boto3.Session(profile_name=profile_name) if profile_name else boto3.Session()
        self.client = self.session.client('sts')

        # If role_arn is provided, assume the role
        if role_arn:
            credentials = self._assume_role(role_arn)
            self.session = boto3.Session(
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken']
            )

    def _assume_role(self, role_arn):
        """
        Assume an IAM role and return the temporary credentials.

        Args:
        - role_arn (str): ARN of the role to assume.

        Returns:
        - dict: Temporary AWS credentials.
        """
        try:
            response = self.client.assume_role(
                RoleArn=role_arn,
                RoleSessionName="AssumeRoleSession"
            )
            return response['Credentials']
        except NoCredentialsError:
            raise ValueError("No AWS credentials found.")
        except Exception as e:
            raise ValueError(f"Failed to assume role: {e}")

    def get_session(self):
        """
        Get the current Boto3 session.

        Returns:
        - boto3.Session: Current Boto3 session.
        """
        return self.session

    def get_resource(self, service_name):
        """
        Get a Boto3 resource for the given service name.

        Args:
        - service_name (str): Name of the AWS service (e.g., "ec2", "s3").

        Returns:
        - boto3.resource: Boto3 resource for the specified service.
        """
        return self.session.resource(service_name)

    def get_client(self, service_name):
        """
        Get a Boto3 client for the given service name.

        Args:
        - service_name (str): Name of the AWS service (e.g., "ec2", "s3").

        Returns:
        - boto3.client: Boto3 client for the specified service.
        """
        return self.session.client(service_name)
