import json

if __name__ == "__main__":
    with open("example.json") as f:
        content = json.load(f)

    print(content["document setup"])
