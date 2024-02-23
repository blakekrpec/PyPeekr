import json
import requests


def requester():
    print("Fetching all sensor ids:")
    resp = requests.get(url="http://192.168.1.149:8085" +
                        "/data.json", timeout=10)
    print(resp)
    print(resp.raw)
    print(resp.text)
    data = json.loads(resp.text)
    return data


def write_to_file(data):
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)


def main():
    data = requester()
    write_to_file(data)


if __name__ == '__main__':
    main()
