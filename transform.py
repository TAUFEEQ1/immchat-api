import json

# Define the input data
with open("./qa.json","r") as f:
    data = json.loads(f.read())

# Create the required schema
schema = {
    "data": [
        {
            "title": "FAQs",
            "paragraphs": []
        }
    ]
}

for item in data:
    paragraph = {
        "context": item["ans"],
        "qas": [
            {
                "id": str(hash(item["qn"])),
                "question": item["qn"]
            }
        ]
    }
    schema["data"][0]["paragraphs"].append(paragraph)

# Print the schema as JSON
with open("./faqs.json","w") as f:
    json.dump(schema,f)
