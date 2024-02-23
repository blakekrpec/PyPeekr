import json
import requests


def requester():
    resp = requests.get(url="http://192.168.1.149:8085" +
                        "/data.json", timeout=10)
    data = json.loads(resp.text)
    return data


def write_to_file(data):
    with open("data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)


def main():
    data = requester()
    write_to_file(data)


if __name__ == '__main__':
    main()
