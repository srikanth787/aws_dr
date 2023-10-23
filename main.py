# main.py

import argparse
from ec2.ec2_details import EC2Details
from utils.logger import CustomLogger
from utils.credentials_handler import CredentialsHandler

logger = CustomLogger(__name__).get_logger()


def main():
    parser = argparse.ArgumentParser(description="Fetch EC2 instance details based on specified criteria.")
    parser.add_argument("--az", required=True, help="Availability zone to filter EC2 instances.")
    parser.add_argument("--account", required=True, help="AWS account ID.")
    parser.add_argument("--region", required=True, help="AWS region.")
    parser.add_argument("--tag_file", default=None, help="Path to file containing tag key-value pairs.")
    parser.add_argument("--profile", default='default', help="AWS CLI profile name. Defaults to 'default'.")

    args = parser.parse_args()

    # Displaying provided command line arguments
    logger.info("Provided Command Line Arguments:")
    for arg, value in vars(args).items():
        logger.info(f"{arg}: {value}")

    try:
        credentials = CredentialsHandler(args.profile)
        session = credentials.get_session()

        ec2_details = EC2Details(session)
        ec2_details.display_instances(args.az, args.account, args.region, args.tag_file)

    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
