import socket
import paramiko
import csv
from concurrent.futures import ThreadPoolExecutor
import logging
import os

logger = logging.getLogger(__name__)

class EC2SSH:
    def __init__(self, private_key_path, output_folder):
        self.private_key_path = private_key_path
        self.output_folder = output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.failed_ips_file = os.path.join(output_folder, 'failed_ssh_ips.csv')

    def _is_port_open(self, ip_address, port=22):
        try:
            with socket.create_connection((ip_address, port), timeout=5):
                return True
        except (socket.timeout, socket.error):
            return False

    def _ssh_to_instance(self, ip_address):
        if not self._is_port_open(ip_address):
            logger.warning(f"Port 22 on {ip_address} is not open. Skipping SSH.")
            self._write_to_failed_file(ip_address, "Port 22 not open")
            return

        key = paramiko.RSAKey.from_private_key_file(self.private_key_path)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(ip_address, username='ec2-user', pkey=key)
            _, stdout, stderr = ssh_client.exec_command('echo "Hello from EC2"')  # Sample command
            response = stdout.read().decode('utf-8').strip()
            logger.info(f"Response from {ip_address}: {response}")
        except Exception as e:
            logger.error(f"Failed to connect to {ip_address}. Error: {str(e)}")
            self._write_to_failed_file(ip_address, str(e))
        finally:
            ssh_client.close()

    def _write_to_failed_file(self, ip_address, reason):
        with open(self.failed_ips_file, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([ip_address, reason])

    def ssh_to_all_instances(self, ip_addresses, max_threads=10):
        with open(self.failed_ips_file, 'w', newline='') as csvfile:  # create or overwrite the file
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['IP Address', 'Failure Reason'])

        with ThreadPoolExecutor(max_threads) as executor:
            executor.map(self._ssh_to_instance, ip_addresses)

if __name__ == "__main__":
    # Test the class
    private_key_path = "path_to_private_key.pem"  # Replace this with the path to your EC2 private key.
    ip_addresses_list = ["ip1", "ip2"]  # Replace with the list of IPs from ec2_details.py's output

    ec2_ssh = EC2SSH(private_key_path, './outputs')
    ec2_ssh.ssh_to_all_instances(ip_addresses_list)
