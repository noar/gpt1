import os
import json
import subprocess

class Recipient:
    def __init__(self, name, email, fingerprint, ip=None, port=None):
        self.name = name
        self.email = email
        self.fingerprint = fingerprint
        self.ip = ip
        self.port = port

    def __str__(self):
        return f"{self.name} <{self.email}> ({self.fingerprint})"

    def get_id(self):
        return self.fingerprint.replace(" ", "")[-8:]

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return Recipient(data["name"], data["email"], data["fingerprint"], data.get("ip"), data.get("port"))

    def to_json(self):
        data = {"name": self.name, "email": self.email, "fingerprint": self.fingerprint}
        if self.ip:
            data["ip"] = self.ip
        if self.port:
            data["port"] = self.port
        return json.dumps(data)

    @staticmethod
    def list_from_file(filename):
        if not os.path.exists(filename):
            return []

        with open(filename) as f:
            return [Recipient.from_json(line.strip()) for line in f if line.strip()]

    @staticmethod
    def list_to_file(filename, recipients):
        with open(filename, "w") as f:
            for recipient in recipients:
                f.write(recipient.to_json() + "\n")

    @staticmethod
    def get_fingerprint(email):
        try:
            output = subprocess.check_output(f"gpg --list-keys {email}", shell=True, stderr=subprocess.STDOUT)
            lines = output.decode().split("\n")
            fingerprint_line = next(line for line in lines if "Key fingerprint" in line)
            return fingerprint_line.split("=")[1].strip()
        except subprocess.CalledProcessError as e:
            return None
