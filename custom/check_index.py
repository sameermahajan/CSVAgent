import pickle

with open("schema_index/index.pkl", "rb") as f:
    data = pickle.load(f)

print(type(data))
print(data.keys())
print("index_to_docstore_id:", data.get("index_to_docstore_id"))
