import paramiko
import socket
from concurrent.futures import ThreadPoolExecutor
from utils.logger import Logger
from utils.utilities import Utilities
import csv

class EC2SSH:

    def __init__(self, account, region, az, private_key_path):
        self.account = account
        self.region = region
        self.az = az
        self.private_key_path = private_key_path
        self.logger = Logger(account, region, az).get_logger()
        self.utilities = Utilities(account, region, az)

    def _can_connect(self, host):
        """Check if host is reachable on port 22."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, 22))
        sock.close()
        return result == 0

    def _ssh_to_instance(self, instance):
        """Attempt to establish an SSH connection to the given instance."""
        ip_address = instance.get('PrivateIpAddress', None)
        if not ip_address:
            return (instance['InstanceId'], 'No Private IP Address')

        if not self._can_connect(ip_address):
            return (instance['InstanceId'], 'Cannot connect to port 22')

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ip_address, username='ec2-user', key_filename=self.private_key_path)
            ssh.close()
            return (instance['InstanceId'], 'SSH Success')
        except Exception as e:
            self.logger.error(f"Failed to SSH into {ip_address}. Error: {str(e)}")
            return (instance['InstanceId'], 'SSH Failed')

    def ssh_to_instances(self, instances):
        """Attempt to SSH into multiple instances in parallel."""
        failed_ssh = []
        with ThreadPoolExecutor() as executor:
            for instance, status in executor.map(self._ssh_to_instance, instances):
                if status != 'SSH Success':
                    failed_ssh.append((instance, status))

        if failed_ssh:
            self._write_failed_ssh_to_csv(failed_ssh)

    def _write_failed_ssh_to_csv(self, failed_instances):
        """Write failed SSH attempts to a CSV file."""
        file_path = self.utilities.get_output_path('failed_ssh.csv')
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Instance ID', 'Reason'])
            for instance_id, reason in failed_instances:
                writer.writerow([instance_id, reason])
        self.logger.info(f"Failed SSH attempts written to: {file_path}")

