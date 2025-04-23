import json
from collections import defaultdict

def combine_documents_by_title(input_path, output_path):
    grouped_docs = defaultdict(list)

    # Step 1: Read and group by title
    with open(input_path, "r", encoding="utf-8") as infile:
        for line in infile:
            doc = json.loads(line.strip())
            title = doc["title"]
            grouped_docs[title].append(doc["text"])

    # Step 2: Combine grouped texts and write new JSONL
    with open(output_path, "w", encoding="utf-8") as outfile:
        for i, (title, texts) in enumerate(grouped_docs.items()):
            combined_doc = {
                "_id": f"merged_doc{i}",
                "title": title,
                "text": "\n".join(texts),
                "metadata": {}
            }
            json.dump(combined_doc, outfile)
            outfile.write("\n")

    print(f"Combined dataset written to: {output_path}")

# File paths
input_path = "/home/sbhavsar/PoisonedRAG/datasets/nq/after_seminar_1.jsonl"  # Update with your path
output_path = "/home/sbhavsar/PoisonedRAG/datasets/nq/combined_by_title_from after_seminar_1.jsonl"

combine_documents_by_title(input_path, output_path)
