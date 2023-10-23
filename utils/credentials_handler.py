# utils/credentials_handler.py

import boto3

class CredentialsHandler:
    def __init__(self, profile_name=None, role_arn=None, session_name=None):
        """
        Initialize the credentials handler for AWS services.

        Parameters:
        - profile_name (str, optional): The AWS CLI profile name.
        - role_arn (str, optional): The ARN of the role to assume. Defaults to None.
        - session_name (str, optional): The session name to use when assuming a role. Defaults to None.
        """
        self.profile_name = profile_name
        self.role_arn = role_arn
        self.session_name = session_name

    def get_session(self):
        """
        Get a boto3 session for the specified profile or by assuming a role.

        Returns:
        boto3.Session: A session for the specified AWS profile or assumed role.
        """
        my_config = boto3.Config(
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )

        # Start a session using profile or default behavior
        session = boto3.Session(profile_name=self.profile_name, config=my_config) if self.profile_name else boto3.Session(config=my_config)

        # If a role ARN is provided, assume that role
        if self.role_arn:
            sts_client = session.client('sts')
            assumed_role = sts_client.assume_role(
                RoleArn=self.role_arn,
                RoleSessionName=self.session_name or 'AssumedRoleSession'
            )
            session = boto3.Session(
                aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
                aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
                aws_session_token=assumed_role['Credentials']['SessionToken'],
                config=my_config
            )

        return session
