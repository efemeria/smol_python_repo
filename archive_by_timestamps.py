# Functions to archive and unarchive based on timestamps.
# Main function should be sending the data and until the endpoint becomes unreachable
# If endpoint is unreachable, archival process begins 
# When endpoint recovers the data is unarchived and sent back to the endpoint using a timestamp of downtime
# To be used with data that is consistently being sent to an endpoint via python script.

import datetime
import gzip
import os

backup_dir="/var/backups/my_backup"


def send_data(data):
# define your endpoint and any other related things to the data you are sending here

def backup(endpoint_available: bool, data, backup_dir: str):
    backup_start_time = 0
    backup_end_time = 0

    if not endpoint_available:
        backup_start_time = datetime.datetime.now()
        while not endpoint_available:
            write_to_backup(data, backup_dir)
            # if needed here you can throttle by adding a 'sleep' statement
            # get new data
            endpoint_available = send_data(data)

    if endpoint_available and backup_start_time != 0:
        backup_end_time = datetime.datetime.now()
        push_from_backup(backup_dir, backup_start_time, backup_end_time)
        send_data()


def write_to_backup(data, backup_dir: str):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'{backup_dir}/backup_{timestamp}.tsm'
    gz_filename = filename + ".gz"

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    with gzip.open(gz_filename, 'wt', encoding='utf-8') as zipfile:
        zipfile.write('\n'.join(data))


def push_from_backup(backup_dir: str, backup_start_time: datetime, backup_end_time: datetime):
    log_files = [f for f in os.listdir(backup_dir) if f.endswith('.tsm.gz')]

    backup_start_time = backup_start_time.replace(microsecond=0)
    backup_end_time = backup_end_time.replace(microsecond=0)

    log_files.sort()

    for file in log_files:
        timestamp = file.replace('backup_', '').replace('.tsm.gz', '')
        if backup_start_time <= datetime.datetime.strptime(timestamp, '%Y-%m-%d_%H-%M-%S') <= backup_end_time:
            with gzip.open(os.path.join(backup_dir, file), 'rb') as f:
                backup_content = f.read().decode('utf-8').split('\n')
            send_data(backup_content)


# Here goes your main function
def main():

    while True:
        try:
            # Send data annd check if endpoint is available
            endpoint_available = send_data(data)
            # Enter the backup function
            backup(endpoint_available, data, backup_dir)
        except <...>


