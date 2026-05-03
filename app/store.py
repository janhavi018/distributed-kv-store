import json
import os
import time

class KVStore:
    def __init__(self, wal_path="app/wal.log"):
        self.store = {}
        self.wal_path = wal_path

        self._replay_wal()

    def _write_to_wal(self, operation, key, value=None):
        self._rotate_log_if_needed()

        with open(self.wal_path, "a") as f:
            log = {
                "op": operation,
                "key": key,
                "value": value
            }
            f.write(json.dumps(log) + "\n")

    def _replay_wal(self):
        if not os.path.exists(self.wal_path):
            return

        with open(self.wal_path, "r") as f:
            for line in f:
                log = json.loads(line.strip())

                if log["op"] == "PUT":
                    self.store[log["key"]] = log["value"]

                elif log["op"] == "DELETE":
                    self.store.pop(log["key"], None)
    
    def _rotate_log_if_needed(self):
        if os.path.exists(self.wal_path) and os.path.getsize(self.wal_path) > 10 * 1024 * 1024:
            new_name = f"{self.wal_path}.{int(time.time())}"
            os.rename(self.wal_path, new_name)

    def put(self, key, value):
        self._write_to_wal("PUT", key, value)
        self.store[key] = value

    def get(self, key):
        return self.store.get(key)

    def delete(self, key):
        self._write_to_wal("DELETE", key)
        return self.store.pop(key, None)