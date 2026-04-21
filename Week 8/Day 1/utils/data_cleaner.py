import json
import matplotlib.pyplot as plt
import os

DATA_DIR = "data"
FILES = ["train.jsonl", "val.jsonl"]
MAX_OUTPUT_TOKENS = 200

def load_data(path):
    with open(path, 'r') as f:
        return [json.loads(line) for line in f]

def token_length(text):
    return len(text.split())

def analyze(data, title):
    lengths = [
        token_length(d["instruction"] + d["input"] + d["output"])
        for d in data
    ]

    print(f"\n{title}")
    print("Max:", max(lengths))
    print("Min:", min(lengths))
    print("Avg:", sum(lengths)/len(lengths))

    plt.hist(lengths, bins=40)
    plt.title(title)
    plt.show()

def clean_data(data):
    cleaned = []
    for d in data:
        if not d["output"].strip():
            continue
        
        if token_length(d["output"]) > MAX_OUTPUT_TOKENS:
            continue
        
        cleaned.append(d)
    
    return cleaned

def save_data(data, path):
    with open(path, "w") as f:
        for d in data:
            f.write(json.dumps(d) + "\n")


if __name__ == "__main__":
    print("Cleaning train + val")

    for file in FILES:
        input_path = os.path.join(DATA_DIR, file)
        output_path = os.path.join(DATA_DIR, file.replace(".jsonl", "_clean.jsonl"))

        print(f"\nProcessing: {file}")
        data = load_data(input_path)
        analyze(data, f"{file} BEFORE cleaning")
        cleaned = clean_data(data)
        analyze(cleaned, f"{file} AFTER cleaning")
        save_data(cleaned, output_path)
        print(f"Saved: {output_path}")

    print("\ntrain + val cleaned successfully!")