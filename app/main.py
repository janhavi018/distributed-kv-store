from fastapi import FastAPI
from app.store import KVStore

app = FastAPI()
kv = KVStore()

@app.put("/put")
def put(key: str, value: str):
    kv.put(key, value)
    return {"status": "ok"}

@app.get("/get/{key}")
def get(key: str):
    value = kv.get(key)
    return {"value": value}

@app.delete("/delete/{key}")
def delete(key: str):
    value = kv.delete(key)
    return {"deleted": value}