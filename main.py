import json
import os

from src.instance import Instance

def main():
    print("Hello from metaheuristics!")


if __name__ == "__main__":
    main()

    for file in [file for file in os.listdir('instances') if file.endswith('.vrp')]:
        path = os.path.join('instances', file)

        instance = Instance.load(path)

        print(json.dumps(vars(instance)))
