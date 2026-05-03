# python
from app.store import KVStore
import os

def test_put_get():
    kv = KVStore()
    kv.put("a", "1")
    assert kv.get("a") == "1"

def test_delete():
    kv = KVStore()
    kv.put("a", "1")
    kv.delete("a")
    assert kv.get("a") is None

def test_wal_recovery():
    wal_file = "test_wal.log"

    # Step 1: write data
    kv = KVStore(wal_file)
    kv.put("a", "1")

    # Step 2: simulate restart
    kv2 = KVStore(wal_file)

    assert kv2.get("a") == "1"

    os.remove(wal_file)