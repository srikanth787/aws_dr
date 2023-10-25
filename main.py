import argparse
from datetime import datetime
from utils.credentials_handler import CredentialsHandler
from utils.utilities import read_tags_from_file
from ec2.ec2_details import EC2Details
from asg.asg_details import ASGDetails
from asg.asg_process_manager import ASGProcessManager
from utils.logger import logger


def main():
    """
    Main execution function for the AWS DR Scripts.

    Based on the provided command-line arguments, this script can:
    - Fetch details of EC2 instances based on certain criteria.
    - Manage (suspend/resume) processes for specified ASGs.
    - Fetch details of ASGs based on certain criteria.

    It uses various utility and handler classes to achieve its functionality.
    """

    # Initialize the argument parser to interpret command-line arguments
    parser = argparse.ArgumentParser(description="AWS DR Scripts")

    # Define the necessary arguments for AWS configurations and operations
    parser.add_argument("--profile", help="AWS profile to use.")
    parser.add_argument("--region", required=True, help="AWS region to target.")
    parser.add_argument("--az", help="AWS Availability Zone to filter resources.")
    parser.add_argument("--assume-role-arn", help="ARN of the AWS role to assume for operations.")
    parser.add_argument("--action", choices=["fetch-ec2", "fetch-asg", "suspend-asg", "resume-asg"], required=True,
                        help="Specify the action to perform.")
    parser.add_argument("--application-tags-file",
                        help="Path to a file containing application tags to filter resources. Each tag should be on a separate line.")

    # Parse the provided arguments
    args = parser.parse_args()

    # If a file containing application tags is specified, read the tags from it
    application_tags = []
    if args.application_tags_file:
        application_tags = read_tags_from_file(args.application_tags_file)

    try:
        # Initialize AWS credentials using either a profile or by assuming a role
        credentials_handler = CredentialsHandler(profile_name=args.profile, assume_role_arn=args.assume_role_arn)

        # Perform the specified action based on the 'action' argument
        if args.action == "fetch-ec2":
            ec2_obj = EC2Details(credentials_handler)
            ec2_obj.fetch_instances(az=args.az, application_tags=application_tags)
        elif args.action == "fetch-asg":
            asg_obj = ASGDetails(credentials_handler)
            asg_obj.fetch_asgs(az=args.az, application_tags=application_tags)
        elif args.action == "suspend-asg":
            asg_manager = ASGProcessManager(credentials_handler)
            asg_manager.suspend_asgs(application_tags=application_tags)
        elif args.action == "resume-asg":
            asg_manager = ASGProcessManager(credentials_handler)
            asg_manager.resume_asgs(application_tags=application_tags)

    except Exception as e:
        # Handle any unexpected exceptions and log them
        logger.error(f"Error occurred during script execution: {e}")

    finally:
        # Log the completion of script execution
        logger.info("Script execution completed.")


if __name__ == "__main__":
    # Script entry point
    main()
