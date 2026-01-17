"""
Synthetic log data generator module.

This module provides functions to generate realistic sysadmin logs
with associated importance labels (1 for important, 0 for not important).
"""

import random


class LogGenerator:
    """
    Generates synthetic sysadmin logs.
    """

    def __init__(self, seed: int = None):
        """
        Initialize the generator with a random seed for reproducibility.

        Args:
            seed (int, optional): The random seed. Defaults to None.
        """
        if seed is not None:
            random.seed(seed)

        self.auth_logs = [
            ("Accepted password for root from 192.168.1.10 port 54321 ssh2", 0),
            ("Failed password for root from 203.0.113.45 port 12345 ssh2", 1),
            ("pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0", 1),
            ("Connection closed by authenticating user root 192.168.1.10 [preauth]", 0),
            ("Invalid user admin from 10.0.0.5 port 56789", 1),
        ]

        self.system_logs = [
            ("systemd[1]: Starting Periodic Command Scheduler...", 0),
            ("systemd[1]: Started Periodic Command Scheduler.", 0),
            ("systemd[1]: kernel-core.service: Main process exited, code=exited, "
             "status=1/FAILURE", 1),
            ("CRON[1234]: (root) CMD ( /usr/bin/find /tmp -mtime +7 -delete)", 0),
            ("kernel: [123.456] EXT4-fs error (device sda1): ext4_lookup:1594: inode #2", 1),
        ]

        self.network_logs = [
            ("iptables: IN=eth0 OUT= MAC=... SRC=192.168.1.1 DST=192.168.1.255 "
             "PROTO=UDP SPT=123 DPT=123", 0),
            ("iptables: BLOCK: SRC=45.33.22.11 DST=192.168.1.100 PROTO=TCP SPT=443 "
             "DPT=54321", 1),
            ("firewalld[567]: [ALERT] Possible DDoS attack detected from 185.12.34.56", 1),
            ("NetworkManager[456]: <info> [1612345678.901] connectivity: check: SUCCESS", 0),
            ("avahi-daemon[234]: Withdrawing address record for 192.168.1.10 on eth0.", 0),
        ]

        all_logs = self.auth_logs + self.system_logs + self.network_logs
        self.important_logs = [log for log in all_logs if log[1] == 1]
        self.not_important_logs = [log for log in all_logs if log[1] == 0]

    def generate_sample(self) -> dict:
        """
        Generate a single log sample with a roughly 10/90 split for importance.

        Returns:
            dict: A dictionary containing 'text' and 'label'.
        """
        # 10% chance of being important (1), 90% chance of not important (0)
        if random.random() < 0.1:
            log_text, label = random.choice(self.important_logs)
        else:
            log_text, label = random.choice(self.not_important_logs)

        return {"text": log_text, "label": label}

    def generate_dataset(self, num_samples: int) -> list:
        """
        Generate a dataset of log samples.

        Args:
            num_samples (int): The number of samples to generate.

        Returns:
            list: A list of dictionaries (log samples).
        """
        return [self.generate_sample() for _ in range(num_samples)]
