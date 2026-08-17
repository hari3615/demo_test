import pickle
import base64

def import_project_from_blob(blob_base64: str):
    # Bandit finding: pickle.loads() to deserialize untrusted input
    # CWE-502 Deserialization of Untrusted Data
    raw_data = base64.b64decode(blob_base64)
    data = pickle.loads(raw_data)
    return data
