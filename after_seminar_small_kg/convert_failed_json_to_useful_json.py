import json
import re

def extract_valid_json_blocks(input_json):
    """
    Extracts valid JSON starting with '{\n  "nodes":' and combines nodes and relationships.
    Assigns `documentId` from outer 'doc_id' and ensures it's NOT duplicated inside `attributes`.
    """
    combined_data = {
        "nodes": [],
        "relationships": []
    }

    json_pattern = re.compile(r'{\s*"nodes":.*}', re.DOTALL)

    for item in input_json:
        response = item.get("response", "")
        doc_id = item.get("doc_id", "unknown_doc")

        match = json_pattern.search(response)
        if match:
            valid_json = match.group(0)
            try:
                parsed_json = json.loads(valid_json)

                # Clean nodes
                for node in parsed_json.get("nodes", []):
                    attributes = node.get("attributes", {})

                    # Remove any duplicate key from attributes
                    for key in ["id", "label", "documentId"]:
                        attributes.pop(key, None)

                    node["documentId"] = doc_id
                    node["attributes"] = attributes
                    combined_data["nodes"].append(node)

                # Clean relationships
                for rel in parsed_json.get("relationships", []):
                    attributes = rel.get("attributes", {})

                    for key in ["id", "label", "documentId"]:
                        attributes.pop(key, None)

                    rel["documentId"] = doc_id
                    rel["attributes"] = attributes
                    combined_data["relationships"].append(rel)

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in chunk {item.get('chunk_index', 'unknown')}: {e}")
        else:
            print(f"No valid JSON found in chunk {item.get('chunk_index', 'unknown')}")

    return combined_data



# File paths
input_json_path = "/home/sbhavsar/PoisonedRAG/after_seminar_small_kg/jsons/23_04_2025_failed_chunks_new_sys.json"  # Input file path
output_json_path = "/home/sbhavsar/PoisonedRAG/after_seminar_small_kg/jsons/23_04_2025_updated_failed_chunks_new_sys.json"   # Output file path

# Load the input JSON
with open(input_json_path, "r") as infile:
    input_data = json.load(infile)

# Extract valid JSON and combine nodes/relationships
output_data = extract_valid_json_blocks(input_data)

# Save the combined data to the output file
with open(output_json_path, "w") as outfile:
    json.dump(output_data, outfile, indent=4)

print(f"Combined data saved to {output_json_path}")
