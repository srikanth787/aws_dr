import boto3


class CredentialsHandler:
    """
    A class that manages AWS Credentials for boto3.
    """

    def __init__(self, profile_name=None, assume_role_arn=None):
        """
        Initialize CredentialsHandler.

        Parameters:
            - profile_name (str): Name of the AWS CLI profile to use.
            - assume_role_arn (str): ARN of the role to assume if needed.
        """
        self.profile_name = profile_name
        self.assume_role_arn = assume_role_arn

    def get_session(self):
        """
        Gets a boto3 session with appropriate credentials.

        Returns:
            boto3.Session: A boto3 session with the right credentials.
        """
        if self.profile_name:
            session = boto3.Session(profile_name=self.profile_name)
        else:
            session = boto3.Session()

        # If an assume_role_arn is provided, assume that role and get a session
        if self.assume_role_arn:
            sts_client = session.client('sts')
            assumed_role = sts_client.assume_role(RoleArn=self.assume_role_arn, RoleSessionName="AssumedSession")
            credentials = assumed_role['Credentials']
            session = boto3.Session(
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken']
            )

        return session
