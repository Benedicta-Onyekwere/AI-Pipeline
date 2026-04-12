import json, csv, sys, os

def serialize_json_to_csv(json_path, csv_path, columns):
    """
    Converts a verified JSON commitment/topic list to a formatted CSV.
    """
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, "r") as f:
        data = json.load(f)

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(columns)
        for item in data:
            row = [item.get(col.lower().replace(" ", "_").replace("/", "_"), item.get(col.lower())) for col in columns]
            # Fallback for common SONA columns if key mapping fails
            if not any(row):
                 row = [
                    item.get("description"),
                    item.get("who"),
                    item.get("amount"),
                    item.get("timeline"),
                    item.get("quote"),
                    item.get("reasoning")
                ]
            writer.writerow(row)
    print(f"Success: {csv_path} generated with {len(data)} entries.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 serialize_csv.py <input.json> <output.csv>")
    else:
        # Default columns for the SONA workflow
        cols = ["Description", "Who/Organisation", "Amount", "Timeline", "Exact Quotes", "Reasoning"]
        serialize_json_to_csv(sys.argv[1], sys.argv[2], cols)
