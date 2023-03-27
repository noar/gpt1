import os
import json
import gnupg
import magic
import requests
from datetime import datetime

class FileShare:
    def __init__(self, json_file):
        self.json_file = json_file
        self.json_data = {}
        self.load_json()

    def load_json(self):
        if os.path.exists(self.json_file):
            with open(self.json_file) as f:
                self.json_data = json.load(f)

    def save_json(self):
        with open(self.json_file, 'w') as f:
            json.dump(self.json_data, f, indent=4)

    def get_recipients(self):
        return self.json_data.get('recipients', [])

    def add_recipient(self, email):
        recipients = self.get_recipients()
        if email not in recipients:
            recipients.append(email)
            self.json_data['recipients'] = recipients
            self.save_json()

    def remove_recipient(self, email):
        recipients = self.get_recipients()
        if email in recipients:
            recipients.remove(email)
            self.json_data['recipients'] = recipients
            self.save_json()

    def send_files(self, files):
        if not files:
            return
        recipients = self.get_recipients()
        if not recipients:
            print("No recipients added")
            return

        gpg = gnupg.GPG()
        fingerprint = self.json_data.get('fingerprint', None)
        if fingerprint is None:
            print("No own fingerprint set")
            return

        for email in recipients:
            public_keys = gpg.search_keys(email, keyserver='hkps://keys.openpgp.org')
            if not public_keys:
                print(f"No public key found for {email}")
                continue
            key = public_keys[0]
            result = gpg.verify_key(key['keyid'])
            if not result.get('valid', False):
                print(f"Invalid key for {email}")
                continue
            with open(files, 'rb') as f:
                encrypted_data = gpg.encrypt_file(f, key['keyid'], always_trust=True)
                if encrypted_data.ok:
                    print(f"{files} encrypted and sent to {email}")
                else:
                    print(f"Failed to encrypt and send {files} to {email}")
