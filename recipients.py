import json
import os.path
import gnupg

class Recipient:
    def __init__(self, name, email, fingerprint):
        self.name = name
        self.email = email
        self.fingerprint = fingerprint

class RecipientList:
    def __init__(self, filepath):
        self.filepath = filepath
        self.recipients = []
        self.gpg = gnupg.GPG()

    def add(self, recipient):
        self.recipients.append(recipient)

    def remove(self, index):
        self.recipients.pop(index)

    def get(self, index):
        return self.recipients[index]

    def count(self):
        return len(self.recipients)

    def load(self):
        if os.path.isfile(self.filepath):
            with open(self.filepath, 'r') as f:
                data = f.read()
                if data:
                    decrypted_data = str(self.gpg.decrypt(data))
                    self.recipients = [Recipient(**r) for r in json.loads(decrypted_data)]

    def save(self):
        with open(self.filepath, 'w') as f:
            data = json.dumps([r.__dict__ for r in self.recipients])
            encrypted_data = str(self.gpg.encrypt(data, self.gpg.list_keys()[0]['fingerprint']))
            f.write(encrypted_data)

    def get_fingerprints(self):
        return [r.fingerprint for r in self.recipients]
