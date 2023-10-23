# utils/credentials_handler.py

import boto3

class CredentialsHandler:
    def __init__(self, profile_name='default'):
        """
        Initialize the credentials handler for AWS services.

        Parameters:
        - profile_name (str, optional): The AWS CLI profile name. Defaults to 'default'.
        """
        self.profile_name = profile_name

    def get_session(self):
        """
        Get a boto3 session for the specified profile.

        Returns:
        boto3.Session: A session for the specified AWS profile.
        """
        my_config = boto3.Config(
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        return boto3.Session(profile_name=self.profile_name, config=my_config)
