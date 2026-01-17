"""
Synthetic log data generator module.

This module provides functions to generate realistic sysadmin logs
with associated importance labels (1 for important, 0 for not important).
"""

import random
import time


class LogGenerator:
    """
    Generates synthetic sysadmin logs with dynamic content.
    """

    def __init__(self, seed: int = None):
        """
        Initialize the generator with a random seed for reproducibility.

        Args:
            seed (int, optional): The random seed. Defaults to None.
        """
        if seed is not None:
            random.seed(seed)

    def _random_ip(self) -> str:
        """Generate a random IPv4 address."""
        return ".".join(str(random.randint(0, 255)) for _ in range(4))

    def _random_port(self) -> int:
        """Generate a random port number."""
        return random.randint(1024, 65535)

    def _random_pid(self) -> int:
        """Generate a random process ID."""
        return random.randint(1, 32768)

    def _random_timestamp(self) -> str:
        """Generate a random timestamp string."""
        # Simple random time within the last 24 hours
        now = time.time()
        past = now - random.randint(0, 86400)
        return time.strftime("%b %d %H:%M:%S", time.localtime(past))

    def _generate_important_log(self) -> str:
        """Generate a single important log (Label 1)."""
        templates = [
            lambda: f"Failed password for root from {self._random_ip()} "
                    f"port {self._random_port()} ssh2",
            lambda: f"pam_unix(sshd:auth): authentication failure; logname= "
                    f"uid=0 euid=0 tty=ssh ruser= rhost={self._random_ip()}",
            lambda: f"Invalid user admin from {self._random_ip()} port {self._random_port()}",
            lambda: f"systemd[{self._random_pid()}]: kernel-core.service: Main process exited, "
                    f"code=exited, status=1/FAILURE",
            lambda: f"kernel: [{random.uniform(10, 1000):.3f}] EXT4-fs error (device sda1): "
                    f"ext4_lookup:{random.randint(1000, 2000)}: inode #{random.randint(1, 100)}",
            lambda: f"iptables: BLOCK: SRC={self._random_ip()} DST=192.168.1.100 "
                    f"PROTO=TCP SPT={self._random_port()} DPT={self._random_port()}",
            lambda: f"firewalld[{self._random_pid()}]: [ALERT] Possible DDoS attack "
                    f"detected from {self._random_ip()}",
        ]
        return random.choice(templates)()

    def _generate_not_important_log(self) -> str:
        """Generate a single not important log (Label 0)."""
        templates = [
            lambda: f"Accepted password for root from {self._random_ip()} "
                    f"port {self._random_port()} ssh2",
            lambda: f"Connection closed by authenticating user root {self._random_ip()} [preauth]",
            lambda: f"systemd[{self._random_pid()}]: Starting Periodic Command Scheduler...",
            lambda: f"systemd[{self._random_pid()}]: Started Periodic Command Scheduler.",
            lambda: f"CRON[{self._random_pid()}]: (root) CMD "
                    f"( /usr/bin/find /tmp -mtime +{random.randint(1, 14)} -delete)",
            lambda: f"iptables: IN=eth0 OUT= MAC=... SRC={self._random_ip()} "
                    f"DST=192.168.1.255 PROTO=UDP SPT={self._random_port()} "
                    f"DPT={self._random_port()}",
            lambda: f"NetworkManager[{self._random_pid()}]: <info> "
                    f"[{time.time():.3f}] connectivity: check: SUCCESS",
            lambda: f"avahi-daemon[{self._random_pid()}]: Withdrawing address record "
                    f"for {self._random_ip()} on eth0.",
        ]
        return random.choice(templates)()

    def generate_sample(self) -> dict:
        """
        Generate a single log sample with a roughly 10/90 split for importance.

        Returns:
            dict: A dictionary containing 'text' and 'label'.
        """
        # 10% chance of being important (1), 90% chance of not important (0)
        timestamp = self._random_timestamp()
        if random.random() < 0.1:
            log_body = self._generate_important_log()
            label = 1
        else:
            log_body = self._generate_not_important_log()
            label = 0

        # Prepend timestamp to make it look like a syslog line
        full_log = f"{timestamp} my-server {log_body}"
        return {"text": full_log, "label": label}

    def generate_dataset(self, num_samples: int) -> list:
        """
        Generate a dataset of log samples.

        Args:
            num_samples (int): The number of samples to generate.

        Returns:
            list: A list of dictionaries (log samples).
        """
        return [self.generate_sample() for _ in range(num_samples)]
