import json

# Paths
input_path = "/home/sbhavsar/PoisonedRAG/after_seminar_small_kg/jsons/23_04_2025_updated_failed_chunks_new_sys.json"
output_path = "/home/sbhavsar/PoisonedRAG/after_seminar_small_kg/jsons/23_04_2025_new_updated_failed_chunks_new_sys.json"

# Load data
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

missing_node_doc_ids = []
missing_rel_doc_ids = []
converted_lists = 0

# Process nodes
for i, node in enumerate(data.get("nodes", [])):
    attributes = node.get("attributes", {})
    
    # # Move documentId if present
    # if "documentId" in attributes:
    #     node["documentId"] = attributes.pop("documentId")
    # else:
    #     missing_node_doc_ids.append(i)

    # Convert any list-type attribute to a string
    for key, value in list(attributes.items()):
        if isinstance(value, list):
            attributes[key] = ", ".join(map(str, value))
            converted_lists += 1

# Process relationships
for i, rel in enumerate(data.get("relationships", [])):
    attributes = rel.get("attributes", {})

    # # Move documentId if present
    # if "documentId" in attributes:
    #     rel["documentId"] = attributes.pop("documentId")
    # else:
    #     missing_rel_doc_ids.append(i)

    # Convert any list-type attribute to a string
    for key, value in list(attributes.items()):
        if isinstance(value, list):
            attributes[key] = ", ".join(map(str, value))
            converted_lists += 1

# Save updated file
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

# Summary
print(f" Cleaned {len(data.get('nodes', []))} nodes and {len(data.get('relationships', []))} relationships.")
print(f"Converted {converted_lists} list attributes into strings.")
print(f" Saved cleaned data to: {output_path}")

if missing_node_doc_ids:
    print(f"⚠️ {len(missing_node_doc_ids)} nodes missing 'documentId' (e.g., at indexes {missing_node_doc_ids[:5]}...)")
if missing_rel_doc_ids:
    print(f"⚠️ {len(missing_rel_doc_ids)} relationships missing 'documentId' (e.g., at indexes {missing_rel_doc_ids[:5]}...)")
