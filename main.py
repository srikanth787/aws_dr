import argparse
from utils.logger import Logger
from utils.credentials_handler import AWSCredentialsHandler
from utils.utilities import Utilities
from ec2.ec2_details import EC2Details
from asg.asg_details import ASGDetails
from ec2.ec2_ssh import EC2SSH


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="AWS DR Scripts")
    parser.add_argument('--action', required=True, choices=['ec2_details', 'asg_details', 'ec2_ssh'],
                        help="Which action to execute")
    parser.add_argument('--profile_name', help="AWS CLI profile name to use")
    parser.add_argument('--region', help="AWS region")
    parser.add_argument('--az', help="AWS Availability Zone")
    parser.add_argument('--tag_file', help="Path to the tag input file")

    args = parser.parse_args()

    # Setting up logger
    logger = Logger().get_logger()

    # Credentials setup
    aws_credentials = AWSCredentialsHandler(args.profile_name, args.region)

    if args.action == 'ec2_details':
        ec2 = EC2Details(aws_credentials, logger)
        ec2.fetch_and_store(args.tag_file, args.az)

    elif args.action == 'asg_details':
        asg = ASGDetails(aws_credentials, logger)
        asg.fetch_and_store(args.tag_file, args.az)

    elif args.action == 'ec2_ssh':
        ssh = EC2SSH(aws_credentials, logger)
        ssh.check_and_ssh(args.tag_file, args.az)

    else:
        logger.error(f"Unsupported action: {args.action}")


if __name__ == "__main__":
    main()
